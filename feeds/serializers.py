from rest_framework import serializers
from feeds.models import *

class FeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feed
        fields = ('id','title', 'htmlUrl', 'xmlUrl')

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id','title', 'feeds')
        depth = 1

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('id','title', 'author', 'link', 'published', 'updated', 'content', 'feed')
        depth = 1
