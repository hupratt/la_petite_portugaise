from django.urls import reverse
from django.contrib import sitemaps
from datetime import datetime
from django.contrib.sitemaps import Sitemap


class PostSitemap(Sitemap):
    import sys
    sys.path.append("..")
    from posts.models import Post
    changefreq = "monthly"
    priority = 0.9
    def items(self):
        import sys
        sys.path.append("..")
        from posts.models import Post
        return Post.objects.all() # pylint: disable=no-member

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
