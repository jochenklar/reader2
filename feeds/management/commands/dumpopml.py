import xml.etree.ElementTree as et

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User

from feeds.models import Category


class Command(BaseCommand):
    help = 'Prints the stored feeds to the command line.'

    def add_arguments(self, parser):
        parser.add_argument('username', help='Dump feeds of this user')

    def handle(self, *args, **options):
        opml = et.Element('opml')
        opml.set('version', '1.0')

        head = et.SubElement(opml, 'head')
        title = et.SubElement(head, 'title')
        title.text = 'Subscriptions'

        body = et.SubElement(opml, 'body')

        try:
            user = User.objects.get(username=options['username'])
        except (IndexError, User.DoesNotExist):
            raise CommandError('No valid username given.')

        for category in Category.objects.filter(user=user):
            categoryNode = et.SubElement(body, 'outline')
            categoryNode.set('title', category.title)
            categoryNode.set('text', category.title)

            for subscription in category.subscriptions.all():
                feedNode = et.SubElement(categoryNode, 'outline')
                feedNode.set('title', subscription.feed.title)
                feedNode.set('text', subscription.feed.title)
                feedNode.set('type', 'rss')
                feedNode.set('xmlUrl', subscription.feed.xmlUrl)
                feedNode.set('htmlUrl', subscription.feed.htmlUrl)

        print(et.tostring(opml).decode())
