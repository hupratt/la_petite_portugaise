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
from posts.models import Post, PostImage
# from django.views.decorators.cache import cache_page
import datetime, pytz
from django.utils import timezone
from .translate import translate
from django.shortcuts import redirect


class list_events(ListView):
    model = Post
    template_name = "event_list.html"
    context_object_name = 'event_listing'

    def get_context_data(self, **kwargs):
        from django.utils.translation import get_language
        context = super().get_context_data(**kwargs)
        language = get_language()
        liste_events_en = Post.objects.all().filter(tag='event')  # pylint: disable=no-member
        if language == 'en':
            context['events'] = liste_events_en
        else:
            import sys
            sys.path.append("..")
            from la_petite_portugaise.translate import translate
            context['events'] = translate(liste_events_en, language)
        return (context)   

def page_redirect(request):
    return redirect('/')

class index(ListView):
    model = Post
    template_name = "index.html"
    context_object_name = 'events_on_index_page'

    def get_context_data(self, **kwargs):
        from django.utils.translation import get_language
        context = super().get_context_data(**kwargs)
        language = get_language()
        liste_events_en = Post.objects.all().filter(tag='event').order_by('timestamp').filter(timestamp__gte = datetime.datetime.now(tz=pytz.timezone(settings.TIME_ZONE)))  # pylint: disable=no-member
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
    # else:
        # form = EmailPostForm()
    return render(request, "contact.html", {'form': form, 'Name_placeholder': _('Name'), 'sent': sent})
