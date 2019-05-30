from django import template
# from django.template import Template
from django.utils.formats import date_format

register = template.Library()

@register.filter(expects_localtime=True, name="formatter")
def format_date(datetime_object):
    # localize time to users
    # import pytz
    # from django.utils.timezone import localtime
    # from django.conf import settings
    # print(localtime(datetime_object, timezone=pytz.timezone(settings.TIME_ZONE)).strftime("%B, %Y"))
    # print(date_format(datetime_object, format="F, Y", use_l10n=True))
    # from django.utils.translation import get_language
    # print(get_language())
    # date = formats.date_format(datetime_object, format="F, Y", use_l10n=True)
    return date_format(datetime_object, format="F, Y", use_l10n=True)

