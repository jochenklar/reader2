from rest_framework import serializers
from feeds.models import *

class FeedSerializer(serializers.ModelSerializer):
    def save_object(self, obj, **kwargs):
        user = self.context['request'].user

        if obj.id == None:
            obj.save()
            obj.users.add()

        if 'categoryId' in self.context['request'].DATA:
            # look for the old cateory for this feed and user
            rows = Category.objects.filter(user=user).filter(feeds__title=obj.title)
            if rows:
                obj.categories.remove(rows[0])
                obj.save()

            obj.categories.add(self.context['request'].DATA['categoryId'])

        obj.save()

    class Meta:
        model = Feed
        fields = ('id','title', 'htmlUrl', 'xmlUrl')
        read_only_fields = ('id',)
        depth = 1

class CategorySerializer(serializers.ModelSerializer):
    def save_object(self, obj, **kwargs):
        obj.user = self.context['request'].user
        obj.save()

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
        read_only_fields = ('id','title', 'author', 'link', 'published', 'updated', 'content', 'feed')
        depth = 1
