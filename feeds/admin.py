from django.contrib import admin
from feeds.models import *

class CategoryAdmin(admin.ModelAdmin):
    ordering = ['id']

class FeedAdmin(admin.ModelAdmin):
    fields = ('title','htmlUrl','xmlUrl','users')
    ordering = ['id']

class ItemAdmin(admin.ModelAdmin):
    ordering = ['id']

admin.site.register(Category, CategoryAdmin)
admin.site.register(Feed, FeedAdmin)
admin.site.register(Item, ItemAdmin)
