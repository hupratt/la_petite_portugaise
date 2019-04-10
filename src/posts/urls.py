from django.conf.urls import url
from . import views
from .views import PostLikeToggle
# from django.conf import settings
# from django.conf.urls.static import static


urlpatterns = [
    url(r'^$', views.list, name = 'home'),
    url(r'^create/$', views.create, name = 'create'),
    url(r'^(?P<id>\d+)/edit/$', views.post_update, name = 'post_update'),
    url(r'^(?P<id>\d+)/$', views.detail, name = 'detail'),
    url(r'^(?P<id>\d+)/delete/$', views.delete, name = 'delete'),
    url(r'^(?P<id>\d+)/like/$', PostLikeToggle.as_view(), name = 'like-toggle'),

    url(r'^contact/$', views.contact, name = 'contact'),
    url(r'^posts/$', views.list, name = 'blog'),
    url(r'^shop/$', views.list, name = 'shop'),

    ]

# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)