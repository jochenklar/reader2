from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError, ParseError

from .models import Category, Feed, Subscription, Item
from .serializers import CategorySerializer, SubscriptionSerializer, ItemSerializer
from .paginations import PageNumberPagination
from .exceptions import FeedException


class CategoryViewSet(viewsets.ModelViewSet):
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.validated_data['user'] = self.request.user
        serializer.save()


class SubscriptionViewSet(viewsets.ModelViewSet):
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = SubscriptionSerializer

    def get_queryset(self):
        return Subscription.objects.filter(category__user=self.request.user)

    def perform_create(self, serializer):
        self._save_feed(serializer)

    def perform_update(self, serializer):
        self._save_feed(serializer)

    def _save_feed(self, serializer):
        category_id = self.request.data.get('categoryId')
        xmlUrl = self.request.data.get('xmlUrl')

        if category_id and xmlUrl:
            # try to find the feed in the database
            try:
                feed = Feed.objects.get(xmlUrl=xmlUrl)
            except Feed.DoesNotExist:
                feed = Feed(xmlUrl=xmlUrl)
                feed.save()
                try:
                    feed.fetchItems()
                except FeedException:
                    feed.delete()
                    raise ParseError()

            # connect the feed to this subscription
            serializer.validated_data['feed'] = feed

            # get the right category
            try:
                serializer.validated_data['category'] = Category.objects.get(id=category_id)
            except Category.DoesNotExist:
                raise ValidationError()

            serializer.save()


class ItemViewSet(viewsets.ModelViewSet):
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = ItemSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        queryset = Item.objects.filter(feed__subscriptions__category__user=self.request.user).distinct()

        feed = self.request.query_params.get('feed', '-1')
        if feed != '-1':
            queryset = queryset.filter(feed=feed)

        return queryset
