from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
import accounts.urls

from tsa.views import index

urlpatterns = patterns('',
    url(r'^$', index, name='home'),
    url(r'^accounts/', include(accounts.urls)),
    url(r'^admin/', include(admin.site.urls)),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)