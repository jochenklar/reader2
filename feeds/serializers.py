from rest_framework import serializers
from feeds.models import *

class CategorySerializer(serializers.ModelSerializer):
    def save_object(self, obj, **kwargs):
        obj.user = self.context['request'].user
        obj.save()

    class Meta:
        model = Category
        fields = ('id','title','subscriptions')
        read_only_fields = ('id','subscriptions')
        depth = 2

class SubscriptionSerializer(serializers.ModelSerializer):
    def save_object(self, obj, **kwargs):
        if u'categoryId' in self.context['request'].DATA and u'xmlUrl' in self.context['request'].DATA:
            category_id = self.context['request'].DATA['categoryId']
            xmlUrl =  self.context['request'].DATA['xmlUrl']

            # try to find the feed in the database
            try:
                feed = Feed.objects.get(xmlUrl=xmlUrl)
                print 'X'
            except Feed.DoesNotExist:
                feed = Feed(xmlUrl=xmlUrl)
                feed.save()
                feed.fetchItems()

            # connect the feed to this subscription
            obj.feed = feed

            # get the right category
            category = Category.objects.get(id=category_id)
            obj.category = category

            obj.save()

    class Meta:
        model = Subscription
        fields = ('id','category','feed')
        read_only_fields = ('id','category','feed')
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
