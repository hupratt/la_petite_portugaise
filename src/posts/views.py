from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from django.contrib import messages
from django.views.generic import RedirectView
from django.http import HttpResponseRedirect, Http404
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.utils import timezone
from django.db.models import Q
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
# from django.contrib.auth import authenticate, login
# from comments.models import Comment
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.core.mail import send_mail
from django.views.generic import ListView


class list(ListView):
    model = Post
    template_name = "event_list.html"
    context_object_name = 'event_listing'

    def get_context_data(self, **kwargs):
        from django.utils.translation import get_language
        context = super().get_context_data(**kwargs)
        language = get_language()
        liste_events_en = Post.objects.all().filter(tag='event').order_by('timestamp')  # pylint: disable=no-member
        if language == 'en':
            context['events'] = liste_events_en
        else:
            import sys
            sys.path.append("..")
            from la_petite_portugaise.translate import translate
            context['events'] = translate(liste_events_en, language)
        return context    

def detail(request, slug):
    """
    Posts method: display the article's detail

    """
    print(slug)
    post = get_object_or_404(Post, slug=slug)
    from django.utils.translation import get_language
    language = get_language()
    import sys
    sys.path.append("..")
    from la_petite_portugaise.translate import translate
    if language == 'en':
        context = {
            "post": post,
            "month_year": post.timestamp.strftime("%B, %Y")
        }
    else:
        context = {
            "post": translate(post, language),
            "month_year": post.timestamp.strftime("%B, %Y")
        }
    return render(request, "event_detail.html", context)  # queryset


class PostLikeToggle(RedirectView):
    """
    Posts method: toggle a like from an article

    """

    def get_redirect_url(self, *args, **kwargs):
        id = self.kwargs.get("id")
        obj = get_object_or_404(Post, id=id)
        url_ = obj.get_absolute_url()
        user = self.request.user
        print(user)
        if user.is_authenticated:
            if user in obj.post_likes.all():
                obj.post_likes.remove(user)
                message = str(user)+" removed a like to id: " + \
                    str(id)+" title: "+str(obj)
                print(message)
                messages.success(self.request, message)
            else:
                obj.post_likes.add(user)
                message = str(user)+" added a like to id: " + \
                    str(id)+" title: "+str(obj)
                print(message)
                messages.success(self.request, message)
        else:
            messages.success(
                self.request, "Log in to be able to comment, like and view all posts")

        return url_
