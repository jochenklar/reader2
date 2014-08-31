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

    paginate_by = 10
    paginate_by_param = 'page_size'

    def get_queryset(self):
        queryset = Item.objects.order_by('-published')

        feed = self.request.QUERY_PARAMS.get('feed', '-1')
        if feed != '-1':
            queryset = queryset.filter(feed=feed)

        return queryset
