import json
import subprocess

from django.conf.urls import url
from django.core.paginator import Paginator, InvalidPage
from django.http import Http404
from tastypie import fields
from tastypie.resources import ModelResource
from tastypie.authorization import Authorization
from tastypie.authentication import Authentication
from tastypie.constants import ALL
from tastypie.utils import trailing_slash
from tastypie.http import HttpNoContent

from api.models import CrawlUrls, CrawlLinks


class UrlResource(ModelResource):
    class Meta:
        queryset = CrawlUrls.objects.all()
        resource_name = 'url'
        allowed_methods = ['get',]
        authorization = Authorization()
        authentication = Authentication()
        filtering = {
            'external': ALL,
            'run_id': ALL,
            'content_type': ALL,
            'status_code': ALL,
        }
        ordering = [
            'timestamp',
        ]
        excludes = ('body',)

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/jobs%s$" % (self._meta.resource_name,
                trailing_slash()), self.wrap_view('jobs'), name="jobs"),
            url(r"^(?P<resource_name>%s)/crawl%s$" % (self._meta.resource_name,
                trailing_slash()), self.wrap_view('crawl'), name="crawl"),
        ]

    def dehydrate_lint_results(self, bundle):
        return json.loads(bundle.data.get('lint_results'))

    def crawl(self, request, **kwargs):
        url = request.GET.get('url')
        follow = request.GET.get('follow')

        if not url:
            raise Http404('A url to crawl must be specified')

        # Start the crawler
        subprocess.Popen([
            '/Users/kderkacz/Projects/Say/seocrawler/.env/bin/python',
            '/Users/kderkacz/Projects/Say/seocrawler/seocrawler.py',
            '--base_url=%s' % url,
            '--database=/Users/kderkacz/Projects/Say/seocrawler/config.yaml',
            '--internal' if follow == 'true' else '',
            ])

        return self.create_response(request, '', response_class=HttpNoContent)

    def jobs(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        self.is_authenticated(request)
        self.throttle_check(request)

        # Do the query.
        query = '''
SELECT c.id
     , c.run_id
     , '' AS body
     , '{}' AS lint_results
     , l.critical AS lint_critical
     , l.error AS lint_error
     , l.warn AS lint_warn
     , l.info AS lint_info
     , l.response_time
     , l.size
  FROM crawl_urls c
     , (SELECT run_id
             , COUNT(1) AS url_count
             , SUM(lint_critical) AS critical
             , SUM(lint_error) AS error
             , SUM(lint_warn) AS warn
             , SUM(lint_info) AS info
             , SUM(response_time) AS response_time
             , SUM(size) AS size
          FROM crawl_urls
         GROUP BY run_id) l
 WHERE c.id IN (SELECT MIN(id) FROM crawl_urls GROUP BY run_id)
   AND c.run_id = l.run_id
        '''

        if 'job' in request.GET:
            # This is very bad. Don't do this -- prone to sql injection
            query += 'AND c.run_id = "%s"' % request.GET.get('job')

        query += '''
 ORDER BY c.id DESC
 LIMIT 5
        '''

        jobs = [job for job in CrawlUrls.objects.raw(query)]
        paginator = Paginator(jobs, 20)

        try:
            page = paginator.page(int(request.GET.get('page', 1)))
        except InvalidPage:
            raise Http404("Sorry, no results on that page.")

        objects = []

        for result in page.object_list:
            bundle = self.build_bundle(obj=result, request=request)
            bundle = self.full_dehydrate(bundle)
            objects.append(bundle)

        object_list = {
            'objects': objects,
        }

        self.log_throttled_access(request)
        return self.create_response(request, object_list)        


class LinkResource(ModelResource):
    to_url = fields.ToOneField(UrlResource, 'to_url', full=True)
    from_url = fields.ToOneField(UrlResource, 'from_url', full=True)

    class Meta:
        queryset = CrawlLinks.objects.all()
        resource_name = 'link'
        allowed_methods = ['get',]
        authorization = Authorization()
        authentication = Authentication()
        filtering = {
            'to_url': ALL,
            'from_url': ALL,
        }

