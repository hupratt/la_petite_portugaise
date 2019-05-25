# -*- coding: utf-8 -*-
# website/context_processors.py
from django.conf import settings
from datetime import datetime
from posts.models import Post


def ga_tracking_id(request):
    return {'ga_tracking_id': settings.GA_TRACKING_ID}


def this_year(request):
    return {'this_year': datetime.today().year}


def facebook_retrieve(request):
    queryset_list = Post.objects.all().filter(title='facebook')  # pylint: disable=no-member
    queryset_list = queryset_list.order_by('-timestamp')[:2]
    return {'facebook_retrieve': queryset_list}


def is_mobile(request):
    # return {'is_mobile': True}
    if 'is_mobile' in request.session:
        return {'is_mobile': request.session['is_mobile']} 
    return {'is_mobile': False}
