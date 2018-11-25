from rest_framework import serializers

from feeds.models import Category, Subscription, Item


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'title', 'subscriptions')
        read_only_fields = ('id', 'subscriptions')
        depth = 2


class SubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscription
        fields = ('id', 'category', 'feed')
        read_only_fields = ('id', 'category', 'feed')
        depth = 1


class ItemSerializer(serializers.ModelSerializer):

    visited = serializers.SerializerMethodField('visited_serializer_method')

    def visited_serializer_method(self, obj):
        if self.context['request'].data and 'visited' in self.context['request'].data:
            if self.context['request'].data['visited'] is True:
                obj.visitedBy.add(self.context['request'].user)
            else:
                obj.visitedBy.remove(self.context['request'].user)

        return self.context['request'].user in obj.visitedBy.all()

    class Meta:
        model = Item
        fields = (
            'id',
            'title',
            'author',
            'link',
            'published',
            'updated',
            'content',
            'feed',
            'visited'
        )
        read_only_fields = (
            'id',
            'title',
            'author',
            'link',
            'published',
            'updated',
            'content',
            'feed'
        )
        depth = 1
