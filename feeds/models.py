import time,datetime,feedparser,urllib2

from django.db import models
from django.utils.timezone import utc
from django.contrib.auth.models import User

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
    updated   = models.DateTimeField(null=True)

    class Meta:
        verbose_name_plural = 'Meta'

class Category(models.Model):
    user          = models.ForeignKey(User)
    title         = models.SlugField(max_length=1024)

    def __unicode__(self):
        return '[' + self.user.username + '] ' + self.title

    class Meta:
        ordering = ['title']

class Subscription(models.Model):
    category  = models.ForeignKey('Category', related_name='subscriptions')
    feed      = models.ForeignKey('Feed', related_name='subscriptions')

    def __unicode__(self):
        return '[' + self.category.user.username + ', ' + self.category.title + '] ' + self.feed.title

class Item(models.Model):
    visitedBy = models.ManyToManyField(User, default=None)

    title     = models.CharField(max_length=1024)
    author    = models.CharField(max_length=1024, blank=True)
    link      = models.URLField(max_length=1024, blank=True)
    published = models.DateTimeField(null=True)
    updated   = models.DateTimeField(null=True, blank=True)
    guid      = models.CharField(max_length=1024)
    content   = models.TextField(blank=True)
    feed      = models.ForeignKey('Feed', related_name='items')
    
    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['-published']

class Feed(models.Model):
    title     = models.CharField(max_length=1024,blank=True)
    htmlUrl   = models.URLField(max_length=1024,blank=True)
    xmlUrl    = models.URLField(max_length=1024)
    updated   = models.DateTimeField(null=True)

    def __unicode__(self):
        return self.xmlUrl

    class Meta:
        ordering = ['title']

    def fetchItems(self):
        # a function converts from feedparser to non-naive django datetime
        def t(timestamp):
            return datetime.datetime.fromtimestamp(time.mktime(timestamp)).replace(tzinfo=utc)

        # fetch feed from the internetz
        try:
            request = urllib2.Request(self.xmlUrl)
            response = urllib2.urlopen(request)
        except urllib2.HTTPError:
            return

        # check status code
        if response.getcode() != 200: return

        # read and parse the feed
        rss = feedparser.parse(response.read())

        if 'title' in rss['feed']:
            self.title = rss['feed']['title']
            self.save()

        if 'link' in rss['feed']:
            self.htmlUrl = rss['feed']['link']
            self.save()

        if 'updated_parsed' in rss['feed']:
            timestamp = t(rss['feed']['updated_parsed'])

        if 'lastBuildDate' in rss['feed']:
            timestamp = t(rss['feed']['lastBuildDate'])

        if self.updated and timestamp < self.updated: return

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
                    item.updated = t(entry['updated_parsed'])
                else:
                    item.updated = datetime.datetime.now().replace(tzinfo=utc)

            except Item.DoesNotExist:
                # create a new model
                item = Item()

                # set guid
                item.guid = guid

                # set published
                if 'updated_parsed' in entry:
                    item.published = t(entry['updated_parsed'])
                elif 'published_parsed' in entry:
                    item.published = t(entry['published_parsed'])
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

            # set corresponding feed model
            item.feed = self

            item.save()

        self.updated = datetime.datetime.utcnow().replace(tzinfo=utc)
        self.save()
