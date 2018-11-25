from django.contrib import admin

from feeds.models import Meta, Category, Subscription, Feed, Item


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'user']


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['feed', 'category']


class FeedAdmin(admin.ModelAdmin):
    list_display = ['title', 'htmlUrl', 'xmlUrl']
    fields = ('title', 'htmlUrl', 'xmlUrl')


class ItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'feed', 'published', 'updated']


admin.site.register(Meta)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(Feed, FeedAdmin)
admin.site.register(Item, ItemAdmin)
