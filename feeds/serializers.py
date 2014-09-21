from rest_framework import serializers
from feeds.models import *

class FeedSerializer(serializers.ModelSerializer):

    def delete_object(self, obj):
        print 'HALLO'

    def save_object(self, obj, **kwargs):
        user = self.context['request'].user

        # append / to feed
        if not obj.xmlUrl.endswith('/'):
            obj.xmlUrl += '/'

        # try to find the feed in the database
        try:
            old_obj = Feed.objects.get(xmlUrl=obj.xmlUrl)
            obj.id = old_obj.id
            obj.title = old_obj.title
            obj.htmlUrl = old_obj.htmlUrl

            # overide the model, will be forgotten at the end of scope
            # the old obj will be returned to the client
            obj = old_obj

        except Feed.DoesNotExist:
            obj.save()
            obj.fetchItems()

        if user not in obj.users.all():
            obj.users.add(user)
            obj.save()

        if 'categoryId' in self.context['request'].DATA:
            # look for the old cateory for this feed and user
            rows = Category.objects.filter(user=user).filter(feeds__title=obj.title)
            if rows:
                obj.categories.remove(rows[0])
                obj.save()

            obj.categories.add(self.context['request'].DATA['categoryId'])


        obj.save()

        # save super machen

    class Meta:
        model = Feed
        fields = ('id','title','htmlUrl','xmlUrl')
        read_only_fields = ('id','title','htmlUrl')
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
        fields = ('id','title','author','link','published','updated','content','feed','visited')
        read_only_fields = ('id','title','author','link','published','updated','content','feed')
        depth = 1
