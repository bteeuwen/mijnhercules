from unidecode import unidecode
import pdb
import os, manage
import re
from datetime import *
import codecs
import csv
import smtplib

from django.core.urlresolvers import reverse 
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib import messages
from django.http import Http404
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, render
from django.contrib.auth.models import User
from django.template import RequestContext
from django.utils import simplejson
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages

from pytz import timezone
import pytz
from mailsnake import *

from .feeds import EventFeed
import mijnhercules.settings as settings
from .models import Match, Location
from .forms import MatchPresence
from members.models import Team, Player, MembershipHercules, Pass
# from mijnhercules.forms import *
from members.forms import EditPlayerForm, ArrangeSubstitutesForm, importMatchesForm, importPlayersForm

SITE_ROOT = os.path.dirname(os.path.realpath(manage.__file__))

eu = pytz.utc

#count amount of teams
# @login_required
# def TeamCount():
#     t = Team.objects.all()
#     return len(t)

def createMatchFeed(request, teamwedstrijd = None):
    cal = EventFeed(teamwedstrijd)
    return cal.__call__(request)   

@login_required
def viewMatch(request, match):
    try:
        m = Match.objects.get(id=match)
    except Match.DoesNotExist:
        raise Http404
    teams = m.getHercules()
    substituteoptions = False
    substitutes = {}
    for t in teams:
        if m.getSubstitutes(t.pk) != 0:
            substituteoptions = True
            substitutes[t] = m.getSubstitutes(t.pk)
    # raise ValueError
    return render(request, 'viewmatch.html', {'match':m, 'hercules':teams, 'substitutes':substitutes, 'substituteoptions':substituteoptions})


def editMatch(request, match):
    u1 = User.objects.get(username=request.user.username)
    teampk = u1.get_profile().team_member.pk
    
    try:
        m = Match.objects.get(id=match)
    except Match.DoesNotExist:
        raise Http404
    if request.method == 'POST' and m.isTeam(teampk):
        form = ArrangeSubstitutesForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            # m.substitutesneeded = cd['substitutesneeded']
            m.setSubstitutes(team = teampk, amountsubsneeded = cd['substitutesneeded'])
            m.save()
            return render(request, 'player/editplayer_complete.html')
    else:
        if m.isTeam(teampk):
            form = ArrangeSubstitutesForm(initial={'substitutesneeded': m.getSubstitutesNeeded(teampk)})
            u1 = User.objects.get(username=request.user.username)
            player = u1.get_profile()
            if player.gender == 'V':
                substituteWilling = Player.women.filter(substitutewilling=True)
            elif player.gender == 'M':
                substituteWilling = Player.men.filter(substitutewilling=True)
            presentplayers = m.getPresentPlayers(player.team_member.pk)
            return render(request, 'match.html', {'match':m, 'form': form, 'substitutes':substituteWilling, 'presentplayers':presentplayers})

        else:
            raise Http404

def readMatch(f):
    # with open(f, 'rU') as csvfile:
        # data = csv.reader(csvfile, delimiter=';', dialect=csv.excel_tab)
        # data.next()
    # data = f.read()
    # data = data.splitlines()
    # dialect = csv.Sniffer().sniff(codecs.EncodedFile(f,"utf-8").read(1024))
    
    f.open() 
    # check whether headers are indicative of a good csv file:
    reader = csv.reader(codecs.EncodedFile(f,"latin-1"), delimiter=';', dialect=csv.excel_tab)
    try:
        assert 'Wedstrijdnummer' and 'Wedstrijddatum (niet geformatteerd)' and 'Aanvangstijd' and 'Aanduiding' and \
        'Thuis team' and 'Uit team' and 'Sport omschrijving' and 'Veld' and 'Accommodatie naam' and 'Plaats' in reader.next()
    except:
        # mail_admins("Foute wedstrijd upload", "Probleem met CSV upload", fail_silently=False)
        return [], "Foutje: het lijkt geen csv bestand te zijn."
    f.close()

    # get min and max daterange so cancelled matches can be deleted later on:
    f.open() 
    data = csv.DictReader(codecs.EncodedFile(f,"latin-1"), delimiter=';', dialect=csv.excel_tab)
    dates = []
    for row in data:
        try:
            date = eu.localize(datetime.strptime((row['Wedstrijddatum (niet geformatteerd)']+" " + row['Aanvangstijd']), '%d-%m-%y %H:%M'))
        except:
            date = eu.localize(datetime.strptime((row['Wedstrijddatum (niet geformatteerd)']+" " + row['Aanvangstijd']), '%d-%m-%Y %H:%M'))
        dates.append(date)
    mindate = min(dates)
    maxdate = max(dates)
    existingmatches = Match.objects.filter(date__lte=maxdate).filter(date__gte=mindate)
    f.close()

    # start saving matches
    savedmatches = []
    f.open() 
    data = csv.DictReader(codecs.EncodedFile(f,"latin-1"), delimiter=';', dialect=csv.excel_tab)
    for row in data:
        if "Zaal" in row['Aanduiding']:
            # add locations if not yet existent in the db
            try:
                loca = re.match(r'(.*)\sveld', row['Veld'])
                hall = loca.group(1)
                loc = Location.objects.get(name=hall)
                #print "Existing", loc
            except:
                loc = re.match(r'(.*)\sveld', row['Veld'])
                loc = Location.objects.create(name=loc.group(1))
                loc.save()
            #add team if not yet existent in the db
            try:
                t1 = Team.objects.get(number=row['Thuis team'])
            except:
                t1 = Team.objects.create(number = row['Thuis team'], level = '99')
                t1.save()
            try:
                t2 = Team.objects.get(number=row['Uit team'])
            except:
                t2 = Team.objects.create(number = row['Uit team'], level = '99')
                t2.save()
            
            # get datetime field:
            try:
                date = eu.localize(datetime.strptime((row['Wedstrijddatum (niet geformatteerd)']+" " + row['Aanvangstijd']), '%d-%m-%y %H:%M'))
            except:
                date = eu.localize(datetime.strptime((row['Wedstrijddatum (niet geformatteerd)']+" " + row['Aanvangstijd']), '%d-%m-%Y %H:%M'))

            #get matches:
            try:
                m = Match.objects.get(nrid=row['Wedstrijdnummer'])
                m.date = date
                m.teamhome = t1
                m.teamaway = t2
                m.location = loc
                m.save()
                savedmatches.append(m)
                #print m
                # saveMatch(m, row[1] + row[2], t1, t2, loc)
            except:
                #print "except match with %s and %s" % (t1, t2)
                m = Match(
                    nrid=row['Wedstrijdnummer'], 
                    date = date,
                    teamhome = t1,
                    teamaway = t2,
                    location = loc)
                m.save()
                savedmatches.append(m)

    # delete cancelled matches:
    for e in existingmatches:
        if e not in savedmatches:
            e.delete()
    f.close()

    return savedmatches, None

def importMatch(request):
    matches = Match.objects.exclude(date__lte=date.today()).order_by('date')
    if request.method == 'POST':
        form = importMatchesForm(request.POST, request.FILES)
        if form.is_valid():
            savedmatches, fail = readMatch(request.FILES['matches'])
         #    request.FILES['matches'].open("rb")
        # portfolio = csv.DictReader(request.FILES['uploadFile'].file)
            return render(request, 'savematch_success.html', {'savedmatches':savedmatches, 'fail': fail})
    else:
        form = importMatchesForm()
    return render(request, 'savematch.html', {'form': form, 'matches': matches})

def viewMyMatches(request):
    u1 = User.objects.get(username=request.user.username)
    teampk = u1.get_profile().team_member.pk
    matches = Match.objects.get_my_matches(teampk)
    presentmatches = {}
    for m in matches:
        if m.playerPresent(teampk, u1):
            status = 'Aanwezig'
        else:
            status = 'Afwezig'
        presentmatches[m] = MatchPresence(initial = status)
    # raise ValueError
    return render(request, 'mymatches.html', {'mymatches': matches, 'presentmatches':presentmatches})

def offerSubstitute(request, matchpk, teampk, substitutepk):
    match = Match.objects.get(pk=matchpk)
    match.addSubstitute(teampk = teampk, player = Player.objects.get(pk=substitutepk))
    messages.add_message(request, messages.SUCCESS, 'Je hebt jezelf aangemeld als mogelijke invaller. Goed bezig!!')
    # return render(request, 'substitutewilling_confirmation.html')
    # redirect_url = reverse(viewMatch, args=matchpk,)
    return redirect(reverse(viewMatch, args=(matchpk,))) 

def cancelSubstituteOffer(request, matchpk, teampk, substitutepk):
    match = Match.objects.get(pk=matchpk)
    match.removeSubstitute(teampk=teampk, player =Player.objects.get(pk=substitutepk))
    # return render(request, 'substitutewilling_cancellation.html')
    messages.add_message(request, messages.SUCCESS, 'Je afmelding als mogelijke invaller is doorgegeven.')
    # return render(request, 'substitutewilling_confirmation.html')
    # redirect_url = reverse(viewMatch, args=matchpk,)
    return redirect(reverse(viewMatch, args=(matchpk,))) 

def addMatchPresence(request, matchpk, teampk, playerpk):
    match = Match.objects.get(pk=matchpk)
    match.addMatchPresence(teampk = teampk, player = Player.objects.get(pk=playerpk))
    messages.add_message(request, messages.SUCCESS, 'Je hebt jezelf aangemeld voor deze wedstrijd!!')
    # return render(request, 'substitutewilling_confirmation.html')
    # redirect_url = reverse(viewMatch, args=matchpk,)
    return redirect(reverse(editMatch, args=(matchpk,))) 

def removeMatchPresence(request, matchpk, teampk, playerpk):
    match = Match.objects.get(pk=matchpk)
    match.removeMatchPresence(teampk=teampk, player =Player.objects.get(pk=playerpk))
    # return render(request, 'substitutewilling_cancellation.html')
    messages.add_message(request, messages.SUCCESS, 'Je afmelding voor deze wedstrijd is doorgegeven.')
    # return render(request, 'substitutewilling_confirmation.html')
    # redirect_url = reverse(viewMatch, args=matchpk,)
    return redirect(reverse(editMatch, args=(matchpk,))) 