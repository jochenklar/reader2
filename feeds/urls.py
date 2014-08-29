from django.conf.urls import patterns, include, url
from rest_framework import routers
from feeds.views import *

router = routers.DefaultRouter()
router.register(r'feeds', FeedViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'items', ItemViewSet)

urlpatterns = patterns('',
    url(r'^', include(router.urls)),
)
