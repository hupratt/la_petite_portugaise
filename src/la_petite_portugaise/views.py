from django.shortcuts import redirect
#from django.http import HttpResponse, HttpResponseRedirect
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


# def handler503(request, exception):
#     return render(request, '503.html', locals())


def index(request):
    """
    Posts method: list all objects on the database + hide draft versions to non-staff users

    """
    queryset_list = Post.objects.all()
    queryset_list = queryset_list.order_by('-timestamp')[:2]

    return render(request, "index.html", {'facebook_retrieve':queryset_list})

def contact(request):
    sent = False 
    queryset_list = Post.objects.all()
    queryset_list = queryset_list.order_by('-timestamp')[:2]

    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            subject = 'New mail from {}'.format(cd['email'])
            message = 'Name {} \nSubject  {} \nMessage  {} \nEmail {} \n'.format(cd['name'], cd['subject'], cd['message'], cd['email'])
            send_mail(subject, message, settings.EMAIL_HOST_USER,[settings.EMAIL_HOST_RECIPIENT])
            sent = True
            messages.success(request,"Your message was successfully sent to: "+settings.EMAIL_HOST_RECIPIENT)
            return HttpResponseRedirect('')
        else:
            messages.error(request,"Your message could not be sent")
            return HttpResponseRedirect('')
    else:
        form = EmailPostForm()
    return render(request, "contact.html", {'form': form,'Name_placeholder': _('Name'), 'facebook_retrieve':queryset_list})


def aboutus(request):
    queryset_list = Post.objects.all()
    queryset_list = queryset_list.order_by('-timestamp')[:2]
    return render(request, "about-us.html", 'facebook_retrieve':queryset_list)