
from datetime import datetime
from django.contrib.sitemaps import Sitemap
 
class PostSitemap(Sitemap):    
	changefreq = "monthly"
	priority = 0.9
 
	def items(self):
		return Post.objects.all()
 
	def lastmod(self, obj):
		return obj.pub_date


from django.contrib import sitemaps
from django.urls import reverse

class StaticViewSitemap(sitemaps.Sitemap):
	priority = 0.9
	changefreq = 'monthly'

	def items(self):
		return ['about-us', 'contact', 'index']

	def location(self, item):
		return reverse(item)
	
	def lastmod(self, obj):
		return datetime.now()