from django import forms
from .models import Post
from pagedown.widgets import PagedownWidget
# from django.contrib.auth.models import User
# from .models import CustomUser
from django.contrib.auth import get_user_model


class PostForm(forms.ModelForm):
    # super(CommentForm, self).__init__(*args, **kwargs)
    # content = forms.CharField(widget=PagedownWidget())
    # self.fields['content'].widget = PagedownWidget() 

    # def __init__(self, user, *args, **kwargs): 
    #     self["content"].required = False
    #     super(PostForm, self).__init__(*args, **kwargs) 
    #     if user:
    #         self.user = user.keys()
    #         print("PostForm self.user",self.user)
    # def get_form_kwargs(self):
    #     kwargs = super(PostForm, self).get_form_kwargs()
    #     kwargs['user'] = self.request.user
    #     print("kwargs['user'] = self.request.user",self.request.user)
    #     return kwargs
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
    object_id= forms.IntegerField(widget=forms.HiddenInput)
    content= forms.CharField(widget=forms.Textarea)

class SubForm2(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = [
            'username'
        ]