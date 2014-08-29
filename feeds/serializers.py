from rest_framework import serializers
from feeds.models import *

class FeedSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Feed
        fields = ('title', 'htmlUrl', 'xmlUrl')

class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ('title', 'feeds')

class ItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Item
        fields = ('title', 'author', 'link', 'published', 'updated', 'guid', 'content', 'feed')
