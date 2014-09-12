from rest_framework import viewsets, generics
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated

from feeds.models import *
from feeds.serializers import *

class FeedViewSet(viewsets.ModelViewSet):
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,)

    queryset = Feed.objects.all()
    serializer_class = FeedSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,)

    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ItemViewSet(viewsets.ModelViewSet):
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,)

    serializer_class = ItemSerializer

    paginate_by = 10
    paginate_by_param = 'page_size'

    def get_queryset(self):
        queryset = Item.objects.order_by('-published')

        feed = self.request.QUERY_PARAMS.get('feed', '-1')
        if feed != '-1':
            queryset = queryset.filter(feed=feed)

        return queryset
