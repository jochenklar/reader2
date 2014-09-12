from django.conf.urls import patterns, include, url
from rest_framework import routers
from feeds.views import *

router = routers.DefaultRouter()
router.register(r'feeds', FeedViewSet, base_name='feed')
router.register(r'categories', CategoryViewSet, base_name='category')
router.register(r'items', ItemViewSet, base_name='item')

urlpatterns = patterns('',
    url(r'^', include(router.urls)),
)
