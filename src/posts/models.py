from django.db import models
from django.conf import settings
from django.urls import reverse
import os
from klingon.models import Translatable
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _
from datetime import datetime
from django.forms import ValidationError


class Post(models.Model, Translatable):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE
    )
    title = models.CharField(max_length=120)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=False)
    slug = models.SlugField(null=False, unique=True, default="event")
    tag = models.CharField(max_length=120, default="event")
    content = models.TextField(null=True, blank=True)
    image = models.FileField(blank=True, null=True)
    draft = models.BooleanField(default=False)
    translatable_fields = ("title", "content")

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title

    @staticmethod
    def get_image_path(instance, filename):
        return os.path.join(
            "photos", str(instance.id), filename
        ) 

    def get_absolute_url(self):
        return reverse(
            "detail", kwargs={"slug": self.slug}
        ) 

    def computelength(instance):  # len_chars_gte_150
        return len(instance.title) > 150 

    class Meta:
        ordering = ["-timestamp", "-updated"]

    def get_like_url(self):
        return reverse(
            "like-toggle", kwargs={"slug": self.slug}
        ) 

    def get_api_like_url(self):
        return reverse(
            "like-api-toggle", kwargs={"slug": self.slug}
        ) 

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title[:49])  

        super(Post, self).save(*args, **kwargs)


class PostImage(models.Model):
    image = models.FileField(blank=True, null=True)
    post = models.ForeignKey("post", on_delete=models.PROTECT)
    created = models.DateTimeField(auto_now_add=True)
    alt = models.CharField(max_length=120, blank=True, null=True)

    def __str__(self):
        return self.alt

    def __unicode__(self):
        return self.alt
