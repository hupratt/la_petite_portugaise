
from django.shortcuts import render, get_object_or_404, redirect
from .forms import EmailPostForm
from .models import Post
# from users.models import CustomUser
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

# from django.views.generic import UpdateView
# from braces.views import LoginRequiredMixin


def list(request):
    """
    Posts method: list all objects on the database + hide draft versions to non-staff users

    """
    return render(request, "posts/index.html") #queryset

def items_per_page(items,p):
    """
    Posts method: complements the list's pagination method by computing the optimal number of posts to display on a given page
    The objective is to have a better slicing of the number of objects that are shown depending on the space they take up 
    
    """
    big = 0
    if type(p) is not int:
        p=1
    for item in items.page(p).object_list:
        if item.big:
            big+=1
    return big


def detail(request, id=id):
    """
    Posts method: display the article's detail: picture, jupyter html notebook and custom html 
    
    """
    instance = get_object_or_404(Post, id=id)
    
    language = request.LANGUAGE_CODE

    new_title = instance.get_translation(language, 'title')
    new_content = instance.get_translation(language, 'content')

    instance.title = new_title
    instance.content = new_content

    initial_data={
        "object_id":instance.id
    }
    content_type = ContentType.objects.get_for_model(Post)
    object_id = instance.id
    article = get_object_or_404(Post, id=object_id)
    if request.user.is_authenticated:
        article.post_views.add(request.user)
    comments = Comment.objects.filter(object_id=object_id, content_type=content_type)
    
    form = SubForm2(request.POST or None)
    comment_form = CommentForm(request.POST or None, initial=initial_data)

    if request.method == 'POST':

        if comment_form.is_valid() and request.user.is_authenticated:
            object_id = comment_form.cleaned_data.get("object_id")
            content = comment_form.cleaned_data.get("content")
            comment, created = Comment.objects.get_or_create(object_id=object_id, content=content, content_type=content_type, user=request.user)
            comment.save()
            # print(instance,id)
            # print(object_id)
            article = get_object_or_404(Post, id=object_id)
            article.post_comments += 1
            article.save()
            messages.success(request,"Successfully saved your comment on the article: {} content: {}".format(instance.title, content))
            return HttpResponseRedirect(comment.content_object.get_absolute_url())      
        if form.is_valid():
            User = get_user_model()
            user, created = User.objects.get_or_create(username=form.cleaned_data.get("username"))
            # user.set_password('hello')
            user.save()
            messages.success(request,"Thank you for subscribing")
            SubForm2()
            # return HttpResponseRedirect('#')
        elif form.errors:
            messages.error(request,"There was an error handling your request")
    context = { 
        "instance":instance,
        "title":'Detail',
        "form":form,
        "comment_form":comment_form,
        "comments":comments,
        "language": language,

    }
    return render(request, "detail.html",context) #queryset


def post_update(request, id=None):
    """
    Posts method: edit the details of a specific article
    
    """
    instance = get_object_or_404(Post, id=id)

    if instance.user.id != request.user.id:
        raise Http404

    language = request.LANGUAGE_CODE
    if language == 'fr':
        title_form = 'Modifier'
    if language == 'en':
        title_form = 'Edit'
        
    form = PostForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid() and request.method == 'POST':
        instance = form.save(commit=False)
        print(form.cleaned_data.get("title"))
        instance.save()
        messages.success(request,"Item sucessfully updated")
        return HttpResponseRedirect(instance.get_absolute_url())
    elif form.errors:
        messages.error(request,"There was an error handling your request")
    context = { 
    #   "instance":instance,
        "is_draft": instance.draft,
        "is_big": instance.big,
        "title":title_form,
        "form":form,
        # "image":instance.image.url,
        # "image2":instance.image2.url,
    }
    return render(request, "edit.html",context) #queryset



# class MyCreateView(LoginRequiredMixin, UpdateView):
#     model = Post
#     form_class = PostForm
#     success_url = "/someplace/"

#     def get_form_kwargs(self):
#         """This method is what injects forms with their keyword
#             arguments."""
#         # grab the current set of form #kwargs
#         kwargs = super(MyUpdateView, self).get_form_kwargs()
#         # Update the kwargs with the user_id
#         kwargs['user_id'] = self.request.user.pk
#         return kwargs


def create(request):
    """
    Posts method: create a new article object
    
    """
    language = request.LANGUAGE_CODE
    if language == 'fr':
        title_form = 'Créer'
    if language == 'en':
        title_form = 'Create'

    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid() and request.method == 'POST':
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        messages.success(request,"Successfully created")
        return HttpResponseRedirect(instance.get_absolute_url())
    elif form.errors:
        messages.error(request,"There was an error handling your request")
    context = { 
    #   "instance":instance,
        "title":title_form,
        "form":form
    }
    return render(request, "edit.html",context) #queryset


def delete(request, id=None):
    """
    Posts method: delete the article that the user is currently viewing
    
    """
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Post, id=id)
    instance.delete()
    messages.success(request,"Item sucessfully deleted")
    return redirect('list')



class PostLikeToggle(RedirectView):
    """
    Posts method: append/remove (aka toggle) a like from an article
    
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
                message = str(user)+" removed a like to id: "+str(id)+" title: "+str(obj)
                print(message)
                messages.success(self.request,message)
            else:
                obj.post_likes.add(user)
                message = str(user)+" added a like to id: "+str(id)+" title: "+str(obj)
                print(message)
                messages.success(self.request,message)  
        else:
            messages.success(self.request,"Log in to be able to comment, like and view all posts")

        return url_



"""
Posts method: should get replaced by a a file drop-in system

"""
def contact(request):
    sent = False 
 
    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            subject = 'New mail from {}'.format(cd['email'])
            message = 'Name {} \nSubject  {} \nMessage  {} \nEmail {} \n'.format(cd['name'], cd['subject'], cd['message'], cd['email'])
            send_mail(subject, message, settings.EMAIL_HOST_USER,['lapetiteportugaise.bxl@gmail.com'])
            sent = True
            messages.success(request,"Your message was successfully sent to: lapetiteportugaise.bxl@gmail.com")
        else:
            messages.error(request,"Your message could not be sent")
    else:
        form = EmailPostForm()
    return render(request, "posts/contact.html", {'form': form,'sent': sent})


