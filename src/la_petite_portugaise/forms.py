from django import forms


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=250, required=True)
    email = forms.EmailField(required=True)
    message = forms.CharField(max_length=2500, required=True)
    subject = forms.CharField(max_length=250, required=True)
