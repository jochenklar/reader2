from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib import admin
admin.autodiscover()

from feeds import urls

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name="layout.html")),
    url(r'^api/', include(urls)),
    url(r'^admin/', include(admin.site.urls))
)
