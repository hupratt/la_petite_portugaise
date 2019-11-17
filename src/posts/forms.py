from django import forms
from .models import Post
from pagedown.widgets import PagedownWidget

# from django.contrib.auth.models import User
# from .models import CustomUser
from django.contrib.auth import get_user_model


class ArticleCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        widgets = {
            "content": PagedownWidget(),
        }
        fields = ["title", "tag", "image", "content"]

    def clean_title(self, title):
        from django.utils.text import slugify
        from django.core.exceptions import ValidationError

        slug = slugify(title)

        if Post.objects.filter(slug=slug).exists():
            raise ValidationError("A post with this title already exists.")

        return title


class CommentForm(forms.Form):
    object_id = forms.IntegerField(widget=forms.HiddenInput)
    content = forms.CharField(widget=forms.Textarea)
