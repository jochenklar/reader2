from rest_framework import serializers
from feeds.models import *

class FeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feed
        fields = ('id','title', 'htmlUrl', 'xmlUrl')

class CategorySerializer(serializers.ModelSerializer):
    def save_object(self, *args, **kwargs):
        args[0].user = self.context['request'].user
        super(CategorySerializer, self).save_object(*args, **kwargs)

    class Meta:
        model = Category
        fields = ('id','title','feeds')
        read_only_fields = ('id','feeds')
        depth = 1

class ItemSerializer(serializers.ModelSerializer):
    visited = serializers.SerializerMethodField('visited_serializer_method')

    def visited_serializer_method(self, obj):
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
