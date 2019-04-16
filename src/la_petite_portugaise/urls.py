"""la_petite_portugaise URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from la_petite_portugaise import views
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import ugettext_lazy as _
from django.contrib.sitemaps.views import sitemap
from .sitemaps import PostSitemap, StaticViewSitemap

sitemaps = {
    'static': StaticViewSitemap,
    # 'posts': PostSitemap
}

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # url(r'^shop/$', views.list, name = 'shop'),
    url(r'sitemap.xml', sitemap, {'sitemaps' : sitemaps } , name='sitemap'),

]

urlpatterns += i18n_patterns(
    url(_('posts/'), include('posts.urls')),
    url(_('about-us/'), views.aboutus, name = 'about-us'),
    url(_('contact/'), views.contact, name = 'contact'),
    url(r'^$', views.index, name = 'index'),

    prefix_default_language=True) 

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)