from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
import xml.etree.ElementTree as et

from feeds.models import Category,Subscription,Feed,Meta

class Command(BaseCommand):
    arg = 'username opmlfile'
    help = 'Imports categories and subscriptions from an OPML file.'

    def handle(self, *args, **options):
        try:
            user = User.objects.get(username=args[0])
        except (IndexError,User.DoesNotExist):
            raise CommandError('No valid username given.')

        try:
            xml = et.parse(args[1])
        except (IndexError,IOError):
            raise CommandError('No valid inputfile given.')

        for categoryNode in xml.find('body').findall('outline'):
            categoryTitle = categoryNode.attrib['title']

            print '    category',categoryTitle

            try:
                category = Category.objects.get(title=categoryTitle,user=user)
            except Category.DoesNotExist:
                category = Category(title=categoryTitle,user=user)
                category.save()

            for subscriptionNode in categoryNode.findall('outline'):
                subscriptionTitle = subscriptionNode.attrib['title']
                subscriptionHtmlUrl = subscriptionNode.attrib['htmlUrl']
                subscriptionXmlUrl = subscriptionNode.attrib['xmlUrl']

                print '        subscription',subscriptionTitle

                try:
                    feed = Feed.objects.get(xmlUrl=subscriptionXmlUrl)
                except Feed.DoesNotExist:
                    feed = Feed(xmlUrl=subscriptionXmlUrl)
                    feed.fetchItems()
                    feed.save()

                try:
                    subscription = Subscription.objects.get(category=category,feed=feed)
                except Subscription.DoesNotExist:
                    subscription = Subscription(category=category,feed=feed)
                    subscription.save()
