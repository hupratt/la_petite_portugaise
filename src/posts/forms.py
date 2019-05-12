from django import forms
from .models import Post
from pagedown.widgets import PagedownWidget
# from django.contrib.auth.models import User
# from .models import CustomUser
from django.contrib.auth import get_user_model


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        widgets = {
            'content': PagedownWidget(),
        }
        fields = [
            'title',
            'ipython',
            'tag',
            'image',
            'image2',
            'draft',
            'big',
            'content',
        ]


class CommentForm(forms.Form):
    object_id = forms.IntegerField(widget=forms.HiddenInput)
    content = forms.CharField(widget=forms.Textarea)
