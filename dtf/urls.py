from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('dtfapp.views',
    url(r'^$', 'people', name='home'),
    url(r'^people/$', 'people', name='people'),
    url(r'^companies/$', 'companies', name='companies'),
)

urlpatterns += patterns('',
    url(r'^admin/', include(admin.site.urls)),
)
