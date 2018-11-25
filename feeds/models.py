import time
import datetime
import feedparser
import requests

from django.db import models
from django.utils.timezone import utc
from django.contrib.auth.models import User

from feeds.exceptions import FeedException


# this is a singleton model
class SingletonModel(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.__class__.objects.exclude(id=self.id).delete()
        super(SingletonModel, self).save(*args, **kwargs)

    @classmethod
    def load(cls):
        try:
            return cls.objects.get()
        except cls.DoesNotExist:
            return cls()


class Meta(SingletonModel):
    updated = models.DateTimeField(null=True)

    class Meta:
        verbose_name_plural = 'Meta'


class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.SlugField(max_length=1024)

    def __str__(self):
        return '[' + self.user.username + '] ' + self.title

    class Meta:
        ordering = ['title']


class Subscription(models.Model):
    category = models.ForeignKey('Category', related_name='subscriptions', on_delete=models.CASCADE)
    feed = models.ForeignKey('Feed', related_name='subscriptions', on_delete=models.CASCADE)

    def delete(self):
        if self.feed.subscriptions.count() <= 1:
            self.feed.delete()
        super(Subscription, self).delete()

    def __str__(self):
        return '[' + self.category.user.username + ', ' + self.category.title + '] ' + self.feed.title


class Item(models.Model):
    visitedBy = models.ManyToManyField(User, default=None)

    title = models.CharField(max_length=1024)
    author = models.CharField(max_length=1024, blank=True)
    link = models.URLField(max_length=1024, blank=True)
    published = models.DateTimeField(null=True)
    updated = models.DateTimeField(null=True, blank=True)
    guid = models.CharField(max_length=1024)
    content = models.TextField(blank=True)
    feed = models.ForeignKey('Feed', related_name='items', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-published']


class Feed(models.Model):
    title = models.CharField(max_length=1024, blank=True)
    htmlUrl = models.URLField(max_length=1024, blank=True)
    xmlUrl = models.URLField(max_length=1024)
    updated = models.DateTimeField(null=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']

    def fetchItems(self):
        # a function converts from feedparser to non-naive django datetime
        def parse_timestamp(timestamp):
            return datetime.datetime.fromtimestamp(time.mktime(timestamp)).replace(tzinfo=utc)

        # fetch feed from the internetz
        try:
            response = requests.get(self.xmlUrl)
        except requests.exceptions.ConnectionError:
            raise FeedException(message='Could not fetch feed for %s' % self.xmlUrl)

        # check status code
        if response.status_code != 200:
            raise FeedException(message='Could not fetch feed for %s' % self.xmlUrl)

        # read and parse the feed
        rss = feedparser.parse(response.content)

        try:
            self.title = rss['feed']['title']
            self.htmlUrl = rss['feed']['link']
            self.save()
        except KeyError:
            raise FeedException(message='Could not parse title/link for %s' % self.xmlUrl)

        timestamp = None

        if 'lastBuildDate' in rss['feed']:
            timestamp = parse_timestamp(rss['feed']['lastBuildDate'])

        if timestamp and self.updated and timestamp < self.updated:
            return

        for entry in rss['entries']:
            # get guid
            if 'guid' in entry:
                guid = entry['guid']
            else:
                guid = entry['link']

            # get corresponding item from the database
            try:
                item = Item.objects.get(guid=guid)

                # set updated
                if 'updated_parsed' in entry:
                    item.updated = parse_timestamp(entry['updated_parsed'])
                else:
                    item.updated = datetime.datetime.now().replace(tzinfo=utc)

            except Item.DoesNotExist:
                # create a new model
                item = Item()

                # set guid
                item.guid = guid

                # set published
                if 'updated_parsed' in entry:
                    item.published = parse_timestamp(entry['updated_parsed'])
                elif 'published_parsed' in entry:
                    item.published = parse_timestamp(entry['published_parsed'])
                else:
                    item.published = datetime.datetime.now().replace(tzinfo=utc)

                # set updated
                item.updated = None

            # set title
            item.title = entry.title

            # set link
            item.link = entry.link

            # set author
            if 'author' in entry:
                item.author = entry['author']
            else:
                item.author = ''

            # set html content
            item.content = ''
            if 'content' in entry:
                for element in entry['content']:
                    if element['type'] == 'text/html':
                        item.content = element['value']
            elif 'description' in entry:
                item.content = entry['description']

            # look for relative links
            item.content = item.content.replace('href="/', 'href="' + item.link + '/')

            # set corresponding feed model
            item.feed = self

            item.save()

        self.updated = datetime.datetime.utcnow().replace(tzinfo=utc)
        self.save()
