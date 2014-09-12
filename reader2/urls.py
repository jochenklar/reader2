from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib import admin
admin.autodiscover()

from feeds import urls

urlpatterns = patterns('',
    url(r'^$', 'reader2.views.index'),
    url(r'^login/$', 'reader2.views.login'),
    url(r'^logout/$', 'reader2.views.logout'),
    url(r'^api/', include(urls)),
    url(r'^admin/', include(admin.site.urls))
)
