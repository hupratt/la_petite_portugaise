from django.db import models
from django.conf import settings
from django.urls import reverse
import os
from klingon.models import Translatable

from django.utils.translation import ugettext_lazy as _

class Post(models.Model, Translatable):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default = 1, on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    ipython = models.FileField(blank=True, null=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=False)
    tag = models.CharField(max_length=120)
    # likes = models.IntegerField(default=0)
    post_likes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='post_likes')
    post_comments= models.IntegerField(default=0)
    # views = models.IntegerField(default=0)
    big = models.BooleanField(default=False)
    content = models.TextField(null=True, blank=True)
    post_views = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='post_views')
    percent_read = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='percent_read')
    image = models.FileField(blank=True, null=True)
    image2 = models.FileField(blank=True, null=True)
    draft = models.BooleanField(default=False)
    translatable_fields = ('title', 'content')

    def __str__(self):
        return self.title
    @staticmethod
    def get_image_path(instance, filename):
        return os.path.join('photos', str(instance.id), filename) #pylint: disable=no-member
    def get_absolute_url(self):
        return reverse("detail", kwargs={"id":self.id}) #pylint: disable=no-member
    class Meta:
        ordering = ['-timestamp','-updated']
    def get_like_url(self):
        return reverse("like-toggle", kwargs={"id": self.id}) #pylint: disable=no-member
    def get_api_like_url(self):
        return reverse("like-api-toggle", kwargs={"id": self.id}) #pylint: disable=no-member


