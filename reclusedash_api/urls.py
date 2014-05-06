from django.conf.urls import patterns, include, url
from tastypie.api import Api

from django.contrib import admin
admin.autodiscover()

from api import UrlResource, LinkResource

v1_api = Api(api_name='v1')
v1_api.register(UrlResource())
v1_api.register(LinkResource())

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'reclusedash_api.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    (r'^api/', include(v1_api.urls)),
)
