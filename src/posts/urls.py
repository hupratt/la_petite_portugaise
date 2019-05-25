from django.conf.urls import url
from . import views
from .views import PostLikeToggle
# from django.conf import settings
# from django.conf.urls.static import static

urlpatterns = [
    url(r'^(?P<id>\d+)/like/$', PostLikeToggle.as_view(), name='like-toggle'),
]


urlpatterns += i18n_patterns(
    url(r'^$', views.index.as_view(), name='index'),
    url(r'^(?P<slug>[-\w\d]+)/', views.detail, name='detail'),

    prefix_default_language=True)