from django.contrib import admin
from accounts.models import Account, Group

# Register your models here.
admin.site.register(Account)
admin.site.register(Group)