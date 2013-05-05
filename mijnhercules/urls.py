from django.contrib.auth.views import login, logout, password_reset
from django.conf.urls.defaults import *
from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView
# Uncomment the next two lines to enable the admin:
from django.contrib import admin

from members.models import Team, Player
from members.views import *
from mijnhercules.views import home

admin.autodiscover()

urlpatterns = patterns('',
	
	# startpagina
	(r'^$', home),

	# url(r'^celery_test/', 'members.views.test_celery'),

	
	url(r'^teams/$', viewTeams),
	url(r'^teams/(?P<team_name>.*)/$', viewTeam),
	
	## individual player url's
	# url(r'^speler/download', PlayerDownload),
	url(r'^speler/wijzigen/(?P<playerid>.*)/$', editPlayer),
	url(r'^speler/wijzigen', editProfile),
	url(r'^speler/sportlink', importPlayers),
	url(r'^speler/migratie', migrate),
	

	# wedstrijden
	url(r'^wedstrijden/', include('matches.urls')),

	# url(r'^api/get_player/', GetPlayer, name='GetPlayer'),
	
	# bestuur: handige administratie overzichten
	url(r'^administratie/emaillozen/', emailLess),
	url(r'^administratie/teamlozen/', TeamLess),
	url(r'^administratie/aanvoerderlozen', captainLess),
	url(r'^administratie/mailchimp', mailchimpExceptions),
	
	# (r'^contact/$', contact),
	# (r'^contact/thanks$', thanks),
	
	## account management
	url(r'^accounts/login/$', login),
	url(r'^accounts/logout/$', logout),
	#url(r'^accounts/password/reset/$', password_reset, {'template_name': 'registration/password_reset.html'}),
	(r'^accounts/password/reset/$', 'django.contrib.auth.views.password_reset', 
        {'post_reset_redirect' : '/accounts/password/reset/done/'}),
	(r'^accounts/password/reset/done/$', 'django.contrib.auth.views.password_reset_done'),
	(r'^accounts/password/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm', 
	        {'post_reset_redirect' : '/accounts/password/done/'}),
	(r'^accounts/password/done/$', 'django.contrib.auth.views.password_reset_complete'),
	
	# admin
	url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
	url(r'^admin/', include(admin.site.urls)),
)