# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from django.contrib import admin
from la_petite_portugaise import views
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import ugettext_lazy as _
from django.contrib.sitemaps.views import sitemap
from .sitemaps import PostSitemap, StaticViewSitemap
from django.views.generic import TemplateView

sitemaps = {
    'static': StaticViewSitemap,
    'posts': PostSitemap
}

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # url(r'^shop/$', views.list, name = 'shop'),
    url(r'^sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),

]

urlpatterns += i18n_patterns(
    url(_('posts/'), include('posts.urls')),
    url(_('about-us/'),
        TemplateView.as_view(template_name="about-us.html"), name='about-us'),
    url(_('contact/'), views.contact, name='contact'),
    url(r'^$', views.index.as_view(), name='index'),

    prefix_default_language=True)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

