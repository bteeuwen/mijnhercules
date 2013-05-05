from django.contrib import admin
# from django.contrib.admin.models import LogEntry, DELETION
from django.utils.html import escape
from django.core.urlresolvers import reverse

from .models import Location, Match

class MatchAdmin(admin.ModelAdmin):
    list_display = ('date', 'nrid', 'teamhome', 'teamaway', 'location')
    list_filter = ['date', 'location']
    search_fields = ['teamaway', 'teamhome']
    list_per_page = 50

admin.site.register(Location)
admin.site.register(Match, MatchAdmin)