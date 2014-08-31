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

        feed = self.request.QUERY_PARAMS.get('feed', '-1')
        if feed != '-1':
            queryset = queryset.filter(feed=feed)

        begin = int(self.request.QUERY_PARAMS.get('begin','1'))
        nrows = int(self.request.QUERY_PARAMS.get('nrows','30'))
        queryset = queryset.order_by('-published')[begin:begin+nrows]

        return queryset