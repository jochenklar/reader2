import datetime
import sys

from django.utils.timezone import utc, now
from django.core.management.base import BaseCommand
from feeds.models import Feed, Meta
from feeds.exceptions import FeedException


class Command(BaseCommand):
    help = 'Fetches the items from all stored feeds.'

    def handle(self, *args, **options):
        for feed in Feed.objects.all():
            print('updating', feed)

            try:
                feed.fetchItems()
            except FeedException as e:
                print('Error: %s' % e.message, file=sys.stderr)

            # clean up everything older than 60 days but keep at least 30 Items
            keep = feed.items.all()[:30].values_list("id", flat=True)
            feed.items.filter(published__lt=(now() - datetime.timedelta(days=60))).exclude(pk__in=list(keep)).delete()

        # if everything went well set the updated field
        meta = Meta.load()
        meta.updated = datetime.datetime.utcnow().replace(tzinfo=utc)
        meta.save()
