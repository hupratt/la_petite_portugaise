
from django.urls import reverse
from django.contrib import sitemaps
from datetime import datetime
from django.contrib.sitemaps import Sitemap
import sys
sys.path.append("..")
from posts.models import Post


class PostSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.9

    def items(self):
        return Post.objects.all()

    def lastmod(self, obj):
        return obj.updated


class StaticViewSitemap(sitemaps.Sitemap):
    priority = 0.9
    changefreq = 'monthly'

    def items(self):
        return ['about-us', 'contact', 'index']

    def location(self, item):
        return reverse(item)

    def lastmod(self, obj):
        return datetime.now()
