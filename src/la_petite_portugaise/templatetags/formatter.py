from django import template
# from django.template import Template
from django.utils import formats

register = template.Library()

@register.filter(expects_localtime=True, name="formatter")
def format_date(datetime_object):
    # localize time to users
    # import pytz
    # from django.utils.timezone import localtime
    # from django.conf import settings
    # print(localtime(datetime_object, timezone=pytz.timezone(settings.TIME_ZONE)).strftime("%B, %Y"))
    # date = formats.date_format(datetime_object, format="F, Y", use_l10n=True)
    return datetime_object

