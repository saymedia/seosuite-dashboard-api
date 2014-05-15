# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines for those models you wish to give write DB access
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
import unicodedata

from django.db import models

class CrawlLinks(models.Model):
    run_id = models.CharField(max_length=36)
    type = models.CharField(max_length=32, blank=True)
    from_url = models.ForeignKey('CrawlUrls', related_name='from_links')
    to_url = models.ForeignKey('CrawlUrls', related_name='to_links')
    link_text = models.CharField(max_length=1024, blank=True)
    alt_text = models.CharField(max_length=1024, blank=True)
    rel = models.CharField(max_length=1024, blank=True)

    class Meta:
        managed = False
        db_table = 'crawl_links'

class CrawlSave(models.Model):
    run_id = models.CharField(max_length=36)
    urls = models.TextField(blank=True)
    url_associations = models.TextField(blank=True)

    class Meta:
        managed = False
        db_table = 'crawl_save'

class CrawlUrls(models.Model):
    run_id = models.CharField(max_length=36)
    level = models.IntegerField()
    content_hash = models.CharField(max_length=64, blank=True)
    address = models.TextField()
    domain = models.CharField(max_length=128, blank=True)
    path = models.TextField(blank=True)
    external = models.IntegerField()
    status_code = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=255, blank=True)
    body = models.TextField(blank=True)
    size = models.IntegerField(blank=True, null=True)
    address_length = models.IntegerField()
    encoding = models.CharField(max_length=16, blank=True)
    content_type = models.CharField(max_length=64, blank=True)
    response_time = models.FloatField(blank=True, null=True)
    redirect_uri = models.CharField(max_length=2048, blank=True)
    canonical = models.CharField(max_length=2048, blank=True)
    title_1 = models.CharField(max_length=1024, blank=True)
    title_length_1 = models.IntegerField(blank=True, null=True)
    title_occurences_1 = models.IntegerField(blank=True, null=True)
    meta_description_1 = models.CharField(max_length=2048, blank=True)
    meta_description_length_1 = models.IntegerField(blank=True, null=True)
    meta_description_occurrences_1 = models.IntegerField(blank=True, null=True)
    h1_1 = models.CharField(max_length=2048, blank=True)
    h1_length_1 = models.IntegerField(blank=True, null=True)
    h1_2 = models.CharField(max_length=2048, blank=True)
    h1_length_2 = models.IntegerField(blank=True, null=True)
    h1_count = models.IntegerField(blank=True, null=True)
    meta_robots = models.CharField(max_length=16, blank=True)
    rel_next = models.CharField(max_length=2048, blank=True)
    rel_prev = models.CharField(max_length=2048, blank=True)
    lint_critical = models.IntegerField(blank=True, null=True)
    lint_error = models.IntegerField(blank=True, null=True)
    lint_warn = models.IntegerField(blank=True, null=True)
    lint_info = models.IntegerField(blank=True, null=True)
    lint_results = models.TextField(blank=True)
    timestamp = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'crawl_urls'

    def __unicode__(self):
        return unicodedata.normalize('NFKD', self.address).encode('ascii', 'ignore')

