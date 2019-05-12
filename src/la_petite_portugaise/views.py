# -*- coding: utf-8 -*-
from django.views.generic import ListView
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


def create_connection_postgres():
    import psycopg2
    import os
    try:
        if os.environ.get('DJANGO_DEVELOPMENT') is not None:
            connection = psycopg2.connect(user=os.environ.get('dbuser'),
                                          password=os.environ.get(
                                              'dbpassword'),
                                          host=os.environ.get('hostipdev'),
                                          port=os.environ.get('pnumber'),
                                          database='lapetiteportugaise')
        else:
            connection = psycopg2.connect(user=os.environ.get('dbuser'),
                                          password=os.environ.get(
                                              'dbpassword'),
                                          host=os.environ.get('hostip'),
                                          port=os.environ.get('pnumber'),
                                          database='lapetiteportugaise')
        cursor = connection.cursor()
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    return cursor, connection


def translate(liste, lang):
    c, conn = create_connection_postgres()
    for post in liste:
        c.execute("SELECT translation FROM klingon_translation WHERE object_id = %s AND lang = %s AND field = %s",
                  (post.pk, lang, 'title'))
        fetch = c.fetchone()
        if fetch is not None and post.title is not None and type(fetch) is tuple:
            post.title = ''.join(fetch)
        c.execute("SELECT translation FROM klingon_translation WHERE object_id = %s AND lang = %s AND field = %s",
                  (post.pk, lang, 'content'))
        fetch = c.fetchone()
        if fetch is not None and post.content is not None and type(fetch) is tuple:
            post.content = ''.join(fetch)
    return liste


class index(ListView):
    model = Post
    template_name = "index.html"
    context_object_name = 'events_first_page'

    def get_context_data(self, **kwargs):
        from django.utils.translation import get_language
        context = super().get_context_data(**kwargs)
        language = get_language()
        liste_events_en = Post.objects.all().filter(tag='event').order_by('timestamp')  # pylint: disable=no-member
        if language == 'en':
            context['events'] = liste_events_en
        else:
            context['events'] = translate(liste_events_en, language)
        return context


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
    return render(request, "contact.html", {'form': form, 'Name_placeholder': _('Name'), 'sent': sent})
