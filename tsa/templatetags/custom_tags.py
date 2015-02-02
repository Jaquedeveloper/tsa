# coding=utf-8

from django import template

from accounts.models import User


register = template.Library()


@register.simple_tag(takes_context=True)
def active(context, tab_name):
    if not context:
        return ''
    if context.get('active_tab') == str(tab_name):
        return 'current'


@register.assignment_tag
def get_group_users(admin):
    users = User.objects.filter(
        account__group=admin.account.group
    ).exclude(pk=admin.pk)

    return users