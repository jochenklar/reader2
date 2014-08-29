from django.db import models
from django.contrib.auth.models import User

class Feed(models.Model):
    users     = models.ManyToManyField(User, related_name='feeds')

    title     = models.CharField(max_length=1024)
    htmlUrl   = models.URLField(max_length=1024)
    xmlUrl    = models.URLField(max_length=1024)
    updated   = models.DateTimeField(null=True)

    def __unicode__(self):
        return self.title

class Category(models.Model):
    user      = models.ForeignKey(User)

    title     = models.SlugField(max_length=1024)
    feeds     = models.ManyToManyField(Feed, related_name='categories')

    def __unicode__(self):
        return self.title

class Item(models.Model):
    visitedBy = models.ManyToManyField(User, default=None)

    title     = models.CharField(max_length=1024)
    author    = models.CharField(max_length=1024)
    link      = models.URLField(max_length=1024)
    published = models.DateTimeField(null=True)
    updated   = models.DateTimeField(null=True)
    guid      = models.CharField(max_length=1024)
    content   = models.TextField()
    feed      = models.ForeignKey('Feed', related_name='items')
    
    def __unicode__(self):
        return self.title
