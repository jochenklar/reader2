from django.conf.urls import patterns, include, url
from rest_framework import routers
from feeds.views import *

router = routers.DefaultRouter()
router.register(r'categories', CategoryViewSet, base_name='category')
router.register(r'subscriptions', SubscriptionViewSet, base_name='subscription')
router.register(r'items', ItemViewSet, base_name='item')

urlpatterns = patterns('',
    url(r'^', include(router.urls)),
)
