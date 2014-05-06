from django.contrib import admin

from api.models import (
    CrawlUrls,
    CrawlLinks,
    )
# Register your models here.
admin.site.register(CrawlUrls)
admin.site.register(CrawlLinks)