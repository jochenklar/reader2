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
    visited = serializers.SerializerMethodField('get_visited')

    def get_visited(self, obj):
        if self.context['request'].DATA and 'visited' in self.context['request'].DATA:
            if self.context['request'].DATA['visited'] == True:
                obj.visitedBy.add(self.context['request'].user)
            else:
                obj.visitedBy.remove(self.context['request'].user)

        return self.context['request'].user in obj.visitedBy.all()

    class Meta:
        model = Item
        fields = ('id','title', 'author', 'link', 'published', 'updated', 'content', 'feed', 'visited')
        depth = 1
