from django.urls import include, path

from rest_framework import routers

from feeds.viewsets import CategoryViewSet, SubscriptionViewSet, ItemViewSet


router = routers.DefaultRouter()
router.register(r'categories', CategoryViewSet, base_name='category')
router.register(r'subscriptions', SubscriptionViewSet, base_name='subscription')
router.register(r'items', ItemViewSet, base_name='item')

urlpatterns = [
    path('', include(router.urls))
]
