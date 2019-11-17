from django.conf.urls import url
from . import views
from .views import PostLikeToggle, ArticleCreate
from django.urls import path

# from django.conf import settings
# from django.conf.urls.static import static

urlpatterns = [
    path("^(?P<slug>[-\w\d]+)/", views.detail, name="detail"),
    path("^(?P<id>\d+)/like/$", PostLikeToggle.as_view(), name="like-toggle"),
    path("edit/", ArticleCreate.as_view(), name="post-edit"),
]

