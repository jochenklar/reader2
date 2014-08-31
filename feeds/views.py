from rest_framework import viewsets, generics
from feeds.models import *
from feeds.serializers import *

class FeedViewSet(viewsets.ModelViewSet):
    queryset = Feed.objects.all()
    serializer_class = FeedSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ItemViewSet(viewsets.ModelViewSet):
    serializer_class = ItemSerializer

    def get_queryset(self):
        queryset = Item.objects.all()

        feedId = self.request.QUERY_PARAMS.get('feedId', None)
        if feedId is not None:
            queryset = queryset.filter(feed=feedId)

        return queryset