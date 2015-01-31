__author__ = 'joker'

from accounts.models import User
from django import template
register = template.Library()

@register.simple_tag(takes_context=True)
def active(context, tab_name):
    if not context:
        return ''
    if context['active_tab'] == str(tab_name):
        return 'current'


@register.assignment_tag
def get_group_users(admin):
    users = User.objects.filter(
        account__group=admin.account.group
    ).exclude(pk=admin.pk)

    return users