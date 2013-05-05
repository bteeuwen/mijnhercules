from django.conf.urls.defaults import *

import matches.views as matches
# from matches.feeds import EventFeed

urlpatterns = patterns('',
    (r'^$', matches.viewMyMatches),
    url(r'^edit/status/aanwezig/(?P<matchpk>[0-9]+)/(?P<teampk>[0-9]+)/(?P<playerpk>[0-9]+)/$', matches.addMatchPresence),
    url(r'^edit/status/afwezig/(?P<matchpk>[0-9]+)/(?P<teampk>[0-9]+)/(?P<playerpk>[0-9]+)/$', matches.removeMatchPresence),
    url(r'^edit/(?P<match>[0-9]+)/$', matches.editMatch),
    url(r'^(?P<match>[0-9]+)/$', matches.viewMatch),
    url(r'^import/$', matches.importMatch),
    url(r'^invallen/(?P<matchpk>[0-9]+)/(?P<teampk>[0-9]+)/(?P<substitutepk>[0-9]+)/$', matches.offerSubstitute),
    url(r'^invallen/tochmaarniet/(?P<matchpk>[0-9]+)/(?P<teampk>[0-9]+)/(?P<substitutepk>[0-9]+)/$', matches.cancelSubstituteOffer),
    # url(r'^invallen/bevestiging', substituteConfirm),
    # matches calender  
    # url(r'^wedstrijden/kalender/(?P<teamwedstrijd>.*)/$', EventFeed()),
    url(r'^kalender/(?P<teamwedstrijd>[0-9]+)/$', matches.createMatchFeed),
    url(r'^kalender/futsal', matches.createMatchFeed),
)