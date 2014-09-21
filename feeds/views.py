from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated

from feeds.models import *
from feeds.serializers import *

class CategoryViewSet(viewsets.ModelViewSet):
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

class SubscriptionViewSet(viewsets.ModelViewSet):
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = SubscriptionSerializer

    def get_queryset(self):
        return Subscription.objects.filter(category__user=self.request.user)

class ItemViewSet(viewsets.ModelViewSet):
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = ItemSerializer

    paginate_by = 10
    paginate_by_param = 'page_size'

    def get_queryset(self):
        queryset = Item.objects.filter(feed__subscriptions__category__user=self.request.user)

        feed = self.request.QUERY_PARAMS.get('feed', '-1')
        if feed != '-1':
            queryset = queryset.filter(feed=feed)

        return queryset
