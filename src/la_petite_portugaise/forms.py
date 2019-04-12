from django import forms
# from django.contrib.auth.models import User
# from .models import CustomUser




# class EmailPostForm(forms.ModelForm):
#     class Meta:
#         model = get_user_model()
#         fields = [
#             'name',
#             'subject',
#             'message',
#             'email'
#         ]


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=250, required=True)
    email = forms.EmailField(required=True)
    message = forms.CharField(max_length=2500, required=True)
    subject = forms.CharField(max_length=250, required=True)
