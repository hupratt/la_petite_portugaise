from django import template
# from django.template import Template

register = template.Library()

@register.filter(expects_localtime=True, name="formatter")
def format_date(date):
    return date.strftime("%B, %Y")