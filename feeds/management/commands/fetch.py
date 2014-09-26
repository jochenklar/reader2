import datetime
from django.utils.timezone import utc
from django.core.management.base import BaseCommand, CommandError
from feeds.models import Feed,Meta

class Command(BaseCommand):
    help = 'Fetches the items from all stored feeds.'

    def handle(self, *args, **options):
        for feed in Feed.objects.all():
            print '    updating',feed
            feed.fetchItems()

        # if everything went well set the updated field
        meta = Meta.load()
        meta.updated = datetime.datetime.utcnow().replace(tzinfo=utc)
        meta.save()
