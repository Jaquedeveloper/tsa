__author__ = 'joker'

from django import template
register = template.Library()

@register.simple_tag(takes_context=True)
def active(context, tab_name):
    if not context:
        return ''
    if context['active_tab'] == str(tab_name):
        return 'current'