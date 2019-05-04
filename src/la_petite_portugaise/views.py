from django.shortcuts import redirect
# from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.shortcuts import render
from .forms import EmailPostForm
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseRedirect, Http404
from posts.models import Post
# from django.views.decorators.cache import cache_page
from datetime import datetime


def contact(request):
    sent = False
    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            subject = 'New mail from {}'.format(cd['email'])
            message = 'Name {} \nSubject  {} \nMessage  {} \nEmail {} \n'.format(
                cd['name'], cd['subject'], cd['message'], cd['email'])
            send_mail(subject, message, settings.EMAIL_HOST_USER,
                      [settings.EMAIL_HOST_RECIPIENT])
            sent = True
            messages.success(
                request, "Your message was successfully sent to: "+settings.EMAIL_HOST_RECIPIENT)
            return HttpResponseRedirect('')
        else:
            messages.error(request, "Your message could not be sent")
            return HttpResponseRedirect('')
    else:
        form = EmailPostForm()
    return render(request, "contact.html", {'form': form, 'Name_placeholder': _('Name')})
