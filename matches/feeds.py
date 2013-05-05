from datetime import timedelta

from django_ical.views import ICalFeed
from django.core.urlresolvers import reverse

from .models import Match
# from .views import viewMatch
import views as m

class EventFeed(ICalFeed):
    """
    A simple event calender
    """
    product_id = '-//example.com//Example//EN'
    timezone = 'Australia/Sydney'


    def __init__(self, teamwedstrijd = None):
        self.team = teamwedstrijd

    def items(self):
        if self.team != None:
            return Match.objects.get_my_matches(self.team)
        return Match.objects.all()

    def item_title(self, item):
        return item

    def item_description(self, item):
        return item

    def item_link(self, item):
        # return '/wedstrijd/' + str(item.id)
        return reverse(m.viewMatch, args=(item.id,))
        # return str(self.team)

    def item_guid(self, item):
        return str(item.nrid)

    # def timezone(self, item):
    #     return str('Europe/Amsterdam')

    def item_location(self, item):
        return item.location.name

    def item_start_datetime(self, item):
        return item.date

    def item_end_datetime(self, item):
        return item.date + timedelta(hours=1)