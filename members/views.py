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

# from members.feeds import EventFeed
import mijnhercules.settings.base as settings
from .models import Team, Player, MembershipHercules, Pass
# Match, Location
# from mijnhercules.forms import *
from .forms import EditPlayerForm, ArrangeSubstitutesForm, importMatchesForm, importPlayersForm, migrationForm


SITE_ROOT = os.path.dirname(os.path.realpath(manage.__file__))

eu = pytz.utc

#count amount of teams
# @login_required
# def TeamCount():
#     t = Team.objects.all()
#     return len(t)

def createUser(p):
    '''
    Creates a username based on player name. Unidecodes characters & strips whitespace.
    Returns nothing.
    '''
    name = str(p)
    name = name.replace(" ", "").lower()
    name = name.decode('utf-8')
    name = unidecode(name)
    account = User.objects.create(username=name)
    p.user = account
    account.email= p.email
    p.save()
    account.save()

@staff_member_required
def viewTeam(request, team_name):
    pk = Team.objects.get(number=team_name)
    team = Player.objects.filter(team_member=pk)
    matchprogram = Match.objects.exclude(date__lte=date.today()).filter(Q(teamhome=pk) | Q(teamaway=pk))
    return render(request, 'team/detail.html', {'team': pk, 'pl_list': team, 'matchprogram':matchprogram})

@staff_member_required
def viewTeams(request):
    teams = Team.objects.filter(number__icontains='Hercules')
    return render(request, 'team/index.html', {'team_list':teams})

@staff_member_required
def emailLess(request):
    emailless = Player.objects.filter(email="").order_by('team_member')
    return render(request, 'administratie/emailloos.html', {'email_less': emailless})

@staff_member_required
def captainLess(request):
    captainless = Team.objects.filter(number__icontains='Hercules').filter(captain=None)
    return render(request, 'administratie/captainloos.html', {'captain_less': captainless})

@staff_member_required
def TeamLess(request):
    teamless = Player.objects.filter(team_member=None)
    return render(request, 'administratie/teamloos.html', {'team_less': teamless})

# @login_required
# def PlayerDetail(request, player):
#     try:
#         player = Player.objects.get(last_name=player)
#     except Player.DoesNotExist:
#         raise Http404
#     return render_to_response('members/player/detail.html', {'player': player})

# @staff_member_required
# def GetPlayer(request, GetPlayer):
#     if request.is_ajax():
#         q = request.GET.get('term', '')
#         playerlist = Player.objects.filter(first_name__icontains = q )[:20]
#         results = []
#         for player in playerlist:
#             player_json = {}
#             player_json['id'] = player.id
#             player_json['label'] = player.first_name
#             player_json['value'] = player.first_name
#             results.append(player_json)
#         data = json.dumps(results)
#     else:
#         data = 'fail'
#     mimetype = 'application/json'
#     return HttpResponse(data, mimetype)

@login_required
def search(request):
    error = False
    if 'q' in request.GET:
        q = request.GET['q']
        if not q:
            error = True
        else:
            players = Player.objects.filter(first_name__icontains=q)
            return render_to_response('player/search_results.html', 
                {'players': players, 'query': q})
    return render_to_response('player/search_form.html', {'error': error})

@login_required
def thanks(request):
    return render(request, 'editplayer_complete.html')

@login_required
def editPlayer(request, playerid):
    p1 = Player.objects.get(id = playerid)
    if request.method == 'POST':
        form = EditPlayerForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            p1.first_name = cd['first_name']
            p1.suffix = cd['suffix']
            p1.last_name = cd['last_name']
            p1.email = cd['email']
            p1.role = cd['role']
            p1.substitutewilling = cd['substitutewilling']
            p1.save()
            return render(request, 'player/editplayer_complete.html')
    else:
        form = EditPlayerForm(
            initial={'email': p1.email, 'first_name': p1.first_name, 'suffix': p1.suffix, 'last_name':p1.last_name, 'substitutewilling': p1.substitutewilling, 'role':p1.role}
        )
    return render(request, 'player/editplayer.html', {'form': form})

@login_required
def editPlayer_complete(request):
    return render(request, 'editplayer_complete.html')

@login_required
def editProfile(request):
    p1 = request.user.player
    ms = MailSnake(settings.MAILCHIMP_API)

    if request.method == 'POST':
        form = EditPlayerForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            p1.first_name = cd['first_name']
            p1.suffix = cd['suffix']
            p1.last_name = cd['last_name']
            p1.email = cd['email']
            p1.role = cd['role']
            p1.substitutewilling = cd['substitutewilling']
            p1.save()
            # now = datetime.nooeuw()
            if cd['nieuwsbrief'] == 'Ingeschreven':
                ms.listSubscribe(apikey=settings.MAILCHIMP_API, id=settings.MAILCHIMP_LIST_ZV, email_address=p1.email, email_type='html', double_optin=False, update_existing=True, replace_interests=False)
            elif cd['nieuwsbrief'] == 'Uitgeschreven':
                ms.listUnsubscribe(apikey=settings.MAILCHIMP_API, id=settings.MAILCHIMP_LIST_ZV, email_address=p1.email, delete_member=False, send_goodbye=True, send_notify=True)
            return render(request, 'player/editplayer_complete.html')
    else:
        try:
            status = ms.listMemberInfo(apikey=settings.MAILCHIMP_API, id=settings.MAILCHIMP_LIST_ZV, email_address = p1.email)['data'][0]['status']
            if status == 'subscribed':
                nieuwsbrief_status = 'Ingeschreven'
            elif status == 'unsubscribed':
                nieuwsbrief_status = 'Uitgeschreven'
        except:
            nieuwsbrief_status = 'UNKNOWN'
        form = EditPlayerForm(
            initial={'email': p1.email, 'first_name': p1.first_name, 'suffix': p1.suffix, 'last_name':p1.last_name, 'role':p1.role, 'substitutewilling': p1.substitutewilling, 'nieuwsbrief':nieuwsbrief_status}
        )
    return render(request, 'player/editprofile.html', {'form': form})

# new subscriptions for waitinglist

## service to download all players for Rob; removed.
# @login_required
# def PlayerDownload(request):
#     # Create the HttpResponse object with the appropriate CSV header.
#     if request.user.is_authenticated() & request.user.has_perm('members.view_player') & request.user.is_active:
#         now = datetime.now()
#         response = HttpResponse(mimetype='text/csv')
#         response['Content-Disposition'] = 'attachment; filename='+str(now.strftime("%Y%m%d-%H%M"))+'.csv'

#         # Create the CSV writer using the HttpResponse as the "file."
#         writer = csv.writer(response)
#         writer.writerow(['KNVB nr', 'Speler', 'Email'])
#         players = Player.objects.all()
#         for p in players:
#             writer.writerow([p.knvbnr, p, p.email])
#         return response
#     else:

#         return HttpResponse("You don't have the appropriate clearance level.")

# function used to import players from sportlink knvb system
def addPlayer(v, knvbnr=None, herculesnr=None, team=None, user=None):
    '''
    A player dictionary ('v') should look like this:   
    {'Achternaam': 'Burger',
     'E-mail': 'bertusburger@hotmail.nl',
     'Geb datum': '23-02-90',
     'Geslacht': 'M',
     'Herculesnummer': '1251',
     'Huisnr': '65',
     'Huisnr toev': '',
     'Lid sinds': '20-03-11',
     'Mobiel': '06-12345678',
     'Postcode': '3513 HK',
     'Registratiedatum': '21-03-13',
     'Relatienr': 'XXJJ973',
     'Roepnaam': 'Bert',
     'Straat': 'Hondenstraat',
     'Telefoon': '',
     'Tussenvoegsels': '',
     'Woonplaats': 'UTRECHT'}
    '''
    if knvbnr==None:
        knvbnr = Pass.objects.create(knvbnr=str(v['Relatienr']))
    
    if herculesnr==None:
        if v['Herculesnummer'] != '':
            # save (hercules) membership specific subscription information
            try: # see if number already exists:
                herculesnr = MembershipHercules.objects.get(herculesnr=str(v['Herculesnummer']))
                # herculesnr.membersince = datetime.strptime(str(v['Lid sinds']), "%d-%m-%y")
                # herculesnr.enrolled = datetime.strptime(str(v['Registratiedatum']), "%d-%m-%y")
                # herculesnr.save()    
            except: # if nonexistent, make up new:
                herculesnr = MembershipHercules.objects.create(herculesnr=str(v['Herculesnummer']))
                # herculesnr.membersince = datetime.strptime(str(v['Lid sinds']), "%d-%m-%y")
                # herculesnr.enrolled = datetime.strptime(str(v['Registratiedatum']), "%d-%m-%y")
                # herculesnr.save()
    
    p1 = Player(
        knvbnr=knvbnr,
        herculesnr=herculesnr,
        team_member=team,

        first_name=v['Roepnaam'],
        suffix=v['Tussenvoegsels'],
        last_name=v['Achternaam'],
        gender=v['Geslacht'],
        age=datetime.strptime(v['Geb datum'], "%d-%m-%y"),
        email=v['E-mail'],
        cellphone=v['Mobiel'],
        regularphone=v['Telefoon'],
        postalcode=v['Postcode'],
        street=v['Straat'],
        streetnr=v['Huisnr'],
        streetnrplus=v['Huisnr toev'],
        city=v['Woonplaats'])

    if user != None:
        u = User.objects.create(username=user, email=v['E-mail'])
        p1.user = u
    elif v['Roepnaam'] and v['Achternaam']:
        if str(v['Tussenvoegsels']) != '':
            u = User.objects.create(username=((v['Roepnaam'] + v['Tussenvoegsels'] + v['Achternaam']).lower().replace(" ", "")))
            p1.user = u
        else:
            u = User.objects.create(username=((v['Roepnaam'] + v['Achternaam']).lower().replace(" ", "")))
            p1.user = u
    else:
        u = User.objects.create(username=v['Relatienr'])
        p1.user = u
    p1.save()

def updatePlayer(v):
    p = Player.object.get(knvbnr__knvbnr=v['Relatienr'])
    p.herculesnr.membersince = datetime.strptime(str(v['Lid sinds']), "%d-%m-%y")
    p.herculesnr.enrolled = datetime.strptime(str(v['Registratiedatum']), "%d-%m-%y")
    p.postalcode=v['Postcode']
    p.street=v['Straat']
    p.streetnr=v['Huisnr']
    p.streetnrplus=v['Huisnr toev']
    p.city=v['Woonplaats']
    p.save()

def removePlayer(pas):
    p1 = Player.objects.get(knvbnr__knvbnr=pas)
    try:
        her = p1.herculesnr
        her.delete()
    except:
        pass
    p1.delete()
    mhpas = Pass.objects.get(knvbnr=pas)
    mhpas.delete()

def playerSync(f1):
    # haal bestaande knvb & hercules nr's op uit mh
    mhpasnrs = Pass.objects.values_list('knvbnr', flat=True)

    mhplayers = Player.objects.all()
    mhplayernames = []
    # sla alle namen op zodat later tijdelijke naar definitieve inschrijving gecheckt kan worden.
    for p in mhplayers:
        mhplayernames.append((p.first_name + p.last_name))

    mhherculesmem = MembershipHercules.objects.all()
    mhherculesnrs = []
    for m in mhherculesmem:
        mhherculesnrs.append(m.herculesnr)

    # Helper functie: rapporteer regel
    def reportPlayer(z):
        result = "%s %s %s %s %s" % (z['Relatienr'], z['Roepnaam'], z['Achternaam'], z['Herculesnummer'],z['E-mail'])
        return result

    def timestamp():
        '''Function to create datetime object to string.'''
        dt_obj = datetime.now()
        date_str = dt_obj.strftime("%Y%m%d%H%M%S")
        return date_str
            
    # open bestand met alle zaalvoetballers 
    zaalvoetballers = []
    zvpas = []
    zvherculesnr = []
    # data = [row for row in csv.reader(f1.read().splitlines())]
    dialect = csv.Sniffer().sniff(codecs.EncodedFile(f1,"utf-8").read(1024))
    f1.open() 
    data = csv.DictReader(codecs.EncodedFile(f1,"utf-8"), delimiter=';', dialect=dialect)
    
    for row in data:
        zaalvoetballers.append(row)
        zvpas.append(row['Relatienr'])
        zvherculesnr.append(row['Herculesnummer'])
    f1.close() 

    # sla alle hercules nummers op die in mh staan
    mislukt = {}
    gelukt = {}
    cases = [   'Hercules nummers toevoegen aan MijnHercules',
                'Hercules nummers teveel in MijnHercules',
                'KNVB nummers teveel in MijnHercules',
                'KNVB voor-inschrijving nieuwe speler (tijdelijk knvb relatienummer)', 
                'KNVB voor-inschrijving nieuwe speler updaten met definitief knvb relatienummer', 
                'KNVB definitieve inschrijving nieuwe speler', 
                'Uitschrijving speler bij Futsal', 
                'Uitschrijving pas',
                'Uitschrijving anders?']
    for c in cases:
        gelukt[c] = []
        mislukt[c] = []

    # # loop alle hercules nummers na
    # for z in zaalvoetballers:
    #     # indien nieuw
    #     if z[9] != '' and z[9] not in mhherculesnrs:
    #         # voeg toe aan mh
    #         h = MembershipHercules(herculesnr = str(z[9])) 
    #         h.save()
    #         gelukt['Hercules nummers toevoegen aan MijnHercules'].append(reportPlayer(z))
    #     # als er geen hercules nummer bekend is:
    #     elif z[9] == '':
    #         # rapporteer zodat Marianne kan bijwerken
    #         mislukt['Hercules nummers toevoegen aan MijnHercules'].append(reportPlayer(z))

    # loop alle knvb nummers na
    # voor ieder sl knvb nr:
    for v in zaalvoetballers:
        
        # if pass is inexistent, it may be new or a replacement of a former temporary pass number.
        if v['Relatienr'] not in mhpasnrs:
            
            # new, temporary pass (5 tot 7 numbers)
            if re.search("(\d{5,7})", v['Relatienr']):
                
                # Sometimes a player is registered twice in SL due to SL sync problems. This should be reported and fixed elsewhere:
                # This is checked by looking up players with a similar name in the import file & logging it.
                for y in zaalvoetballers:
                    if (y['Roepnaam'] + y['Tussenvoegsels'] + y['Achternaam'] + y['Geslacht']) == (v['Roepnaam'] + v['Tussenvoegsels'] + v['Achternaam'] + v['Geslacht']) and y['pas'] != v['pas']:
                        mislukt['KNVB voor-inschrijving nieuwe speler (tijdelijk knvb relatienummer)'].append(reportPlayer(y))        

                ## this is always executed? so problems above always lead to enrollment?
                # unknown temporary subscription"
                # voeg toe aan mh
                addPlayer(v)
                gelukt['KNVB voor-inschrijving nieuwe speler (tijdelijk knvb relatienummer)'].append(reportPlayer(v))

            else:
                # player already exists in MH with temporary subscription, but subscription is made definitive.
                # controleer of er een tijdelijke inschrijving in MH staat op basis van voor- en achternaam.
                if (str(v['Roepnaam']) + str(v['Achternaam'])) in mhplayernames:
                    # Update tijdelijke inschrijvingsnummer met definitieve nummer:"
                    p1 = Player.objects.get(first_name=str(v['Roepnaam']), last_name=str(v['Achternaam']))
                    pasnr = p1.knvbnr
                    pkpass = Pass.objects.create(knvbnr=str(v['pas']))
                    p1.knvbnr = pkpass 
                    addPlayer(v)
                    gelukt['KNVB voor-inschrijving nieuwe speler updaten met definitief knvb relatienummer'].append(reportPlayer(v))

                # if completely new definitive pass number, than add new definitive subscription:
                else:
                    addPlayer(v)
                    gelukt['KNVB definitieve inschrijving nieuwe speler'].append(reportPlayer(v))

        # if pass number already exists in MH:
        elif v['Relatienr'] in mhpasnrs:
            
            # pasnr = Pass.objects.get(knvbnr__=v['Relatienr'])
            p1 = Player.objects.get(knvbnr__knvbnr=v['Relatienr'])
            
            ## update hercules number if current player in MH has none:
            if p1.herculesnr == None and v['Herculesnummer'] != '':
                hnr = MembershipHercules.objects.get(herculesnr = str(v['Herculesnummer']))
                p1.herculesnr = hnr
                p1.save()

    # Remove players that have quit playing futsal.
    # for every pas number in MH passes:
    for mv in mhpasnrs:
        
        # if pas doesn't exist in import file:
        if mv not in zvpas:

            # try retrieving player with this pass:
            try:
                p1 = Player.objects.get(knvbnr__knvbnr=mv)
                p1.delete()
                gelukt['Uitschrijving speler bij Futsal'].append(p1)
            # maybe pass is not linked to a player, than only the pass will be removed;
            except:
                pass
            mhpas = Pass.objects.get(knvbnr=mv)
            mhpas.delete()
            gelukt['Uitschrijving pas'].append(mhpas)
        
        # if pass exists in import file, continue:            
        elif mv in zvpas:
            pass
        
        # weird other situation:
        else:
            mislukt['Uitschrijving anders?'].append(mv)
    
    # after the import rounds, make a final check if existing passes & hercules numbers are linked to players:

    # get existing passes & hercules numbers from MH:
    def cleanHerculesNrs(importHerculesNrs):
        mhherculesnrs = MembershipHercules.objects.values_list('herculesnr', flat=True)
        # print importHerculesNrs
        for h in mhherculesnrs:
        #     print "%s in import? %s. %s not in import? %s" % (h, h in importHerculesNrs, h, h not in importHerculesNrs)
            if str(h) not in importHerculesNrs:
                print MembershipHercules.objects.get(herculesnr = h)
                try:
                    p = Player.objects.get(MembershipHercules__herculesnr=h).delete()
                    print MembershipHercules.objects.filter(herculesnr = h)
                    MembershipHercules.objects.filter(herculesnr = h).delete()
                except:
                    #print "no one found"
                    MembershipHercules.objects.filter(herculesnr = h).delete()
                    gelukt['Hercules nummers teveel in MijnHercules'].append(h)

    print len(zvherculesnr), MembershipHercules.objects.count()
    cleanHerculesNrs(zvherculesnr)

    mhpasnrs = Pass.objects.values_list('knvbnr', flat=True)

    for h in mhpasnrs:
        if h not in zvpas:
            try:
                p = Player.objects.get(knvbnr__knvbnr=h).delete()
                Pass.objects.get(knvbnr=h).delete()
            except:
                #print "no one found"
                Pass.objects.get(knvbnr=h).delete()
                gelukt['KNVB nummers teveel in MijnHercules'].append(h)


    # Verification amount of passes, hercules numbers and players is equal:
    herculesidcount = MembershipHercules.objects.count()
    playercount = Player.objects.count()
    passcount = Pass.objects.count()
    assert (herculesidcount == playercount  ==  passcount) == True, "Aantal spelers (%s), passen  (%s) en Hercules id's  (%s) is niet gelijk" % (playercount, passcount, herculesidcount)

    ## Saving a log:
    # filename = '/scripts/logs/sportlink_sync_' + timestamp() + ".txt"
    # out_file = open(filename, "w")
    # out_file.write("--- SUCCEEDED ----\n")

    print "--- Gelukt ---"
    for k,v in gelukt.iteritems():
        print k, v
    print "--- Mislukt ---"
    for k,v in mislukt.iteritems():
        print k, v

    # for k,val in gelukt.iteritems():
    #     #print k
    #     out_file.write(" *** " + k + "\n")
    #     for v in val:
    #         out_file.write(str(v) + "\n")
    #     out_file.write("\n\n")

    # out_file.write("\n")

    # out_file.write("--- FAILED ----\n")
    # for k,val in mislukt.iteritems():    
    #     #print k
    #     out_file.write(" *** " + k + "\n")
    #     for v in val:
    #         out_file.write(str(v) + "\n")
    #     out_file.write("\n\n")
    # out_file.close()

    # voor ieder knvb nummer:
        # als tijdelijk inschrijvingsnummer is: (6 getallen in plaats van combinatie getal/letter)
            # als er een ander nr is van iemand met dezelfe naam & geboortedatum
                # update speler's knvb nr
                # tel 1 extra aantal bijgewerkte voorinschrijvingen
            # als er geen ander knvb nr is:
                # maak nieuwe speler aan
                # tel & rapporteer 1 extra aantal voorinschrijvingen
        # als definitief inschrijvingsnummer is:
            # als nog niet voorkomt in mh:
                # maak nieuwe speler aan
                # tel aantal definitieve inschrijving
            # als al in mh
                # als mh afwijkend hercules nr heeft (geen in plaats van wel, of ander):
                    # update hercules nummer


    # voor alle knvb nummers in mh:
        # als niet in SL bestand:
            # als in sl oud leden bestand:
                # zet speler op non-actief 
                # tel als uitschrijving
            # als wel in sl alle leden bestand, maar zonder zaal spelactiviteit
                # zet speler op non-actief
                # tel als gestopt met zaalvoetbal
            # rapporteer als afwijking

@staff_member_required
def importPlayers(request):
    if request.method == 'POST':
        form = importPlayersForm(request.POST, request.FILES)
        if form.is_valid():
            playerSync(request.FILES['playerszv'])
            return render(request, 'saveplayers_success.html')
    else:
        form = importPlayersForm()
    return render(request, 'saveplayers.html', {'form': form})

@staff_member_required
def migrate(request):
    if request.method == 'POST':
        form = migrationForm(request.POST, request.FILES)
        if form.is_valid():
            fullMigration(file1 = request.FILES['alldata'], file2= request.FILES['teamcaptains'])
            return render(request, 'saveplayers_success.html')
    else:
        form = migrationForm()
    return render(request, 'migratie.html', {'form': form})

def mailchimpExceptions(request):
    ms = MailSnake(settings.MAILCHIMP_API)
    pl = Player.objects.all()
    exceptions = {}
    emaillessplayers = 0
    for p in pl:
        if p.email:
            try:
                status = ms.listMemberInfo(apikey=settings.MAILCHIMP_API, id=settings.MAILCHIMP_LIST_ZV, email_address = p.email)['data'][0]['status']
                if status != 'subscribed':
                    exceptions[p.email] = status    
            except:
                exceptions[p.email] = 'Failed'
        elif not p.email:
            emaillessplayers += 1
    return render(request, 'administratie/mailchimpstatus.html', {'exceptions': exceptions, 'emaillesscount':emaillessplayers})

# def logMailchimpExceptions():
#     ms = MailSnake(settings.MAILCHIMP_API)
#     # pl = Player.objects.all()
#     pl = Player.objects.filter(email='bteeuwen@gmail.com')
#     exceptions = {}
#     emaillessplayers = 0
#     for p in pl:
#         if p.email:
#             try:
#                 status = ms.listMemberInfo(apikey=settings.MAILCHIMP_API, id=settings.MAILCHIMP_LIST_ZV, email_address = p.email)['data'][0]['status']
#                 if status != 'subscribed':
#                     exceptions[p.email] = status    
#             except:
#                 exceptions[p.email] = 'Failed'
#         elif not p.email:
#             emaillessplayers += 1
#     def timestamp():
#         '''Function to create datetime object to string.'''
#         dt_obj = datetime.now()
#         date_str = dt_obj.strftime("%Y%m%d%H%M%S")
#         return date_str

#     filename = settings.SITE_ROOT + '/scripts/logs/mailchimp_fouten_' + timestamp() + ".txt"
#     out_file = open(filename, "w")
#     for k, v in exceptions.iteritems():
#         out_file.write(k, v + '\n')
#     out_file.close()

# Celery test
# from . import tasks
 
# def test_celery(request):
#     # result = tasks.sleeptask.delay(10)
#     result = tasks.log_mailchimpexceptions.delay()
#     # result_one = tasks.sleeptask.delay(10)
#     # result_two = tasks.sleeptask.delay(10)
#     return HttpResponse(result.task_id)

def fullMigration(file1, file2):
    # open CSV file with all members model data
    # make sure each row is read as a dictionary, with the header defining the keys and the rows the keys values.
    data = csv.DictReader(codecs.EncodedFile(file1,"latin-1"), delimiter=',', dialect=csv.excel_tab)
    data2 = csv.DictReader(codecs.EncodedFile(file2,"latin-1"), delimiter=',', dialect=csv.excel_tab)

    # check whether headers are indicative of a good csv file:
    necessaryfields = ['Herculesnummer','type_inschrijving','blessure','Lid sinds','Registratiedatum','betaald','Relatienr','pasverloop','passtatus','team_member','teamlevel','teamwisseldagen',' teamaanvoerder','user','Roepnaam','Tussenvoegsels','Achternaam','Geslacht','Geb datum','E-mail','Mobiel','Telefoon','Postcode','Woonplaats','Straat','Huisnr','Huisnr toev','role','substitutewilling']
    data_fieldnames =  data.fieldnames
    for f in necessaryfields:
        assert (f in data.fieldnames) == True, "%s is not present in the csv" % f

    necessaryfields2 = ['team','captainknvbnr']
    data2_fieldnames =  data2.fieldnames
    for f in necessaryfields2:
        assert (f in data2.fieldnames) == True, "%s is not present in the csv" % f

    # check whether zero players exist = indication of a clean database.
    assert (Player.objects.count() == 0) == True, "De database is niet leeg: er zijn al %s spelers." % Player.objects.count()

    # Erase existing data #DANGEROUS.
    Team.objects.all().delete()
    Pass.objects.all().delete()
    MembershipHercules.objects.all().delete()
    Player.objects.all().delete()
    User.objects.all().delete()

    for row in data:
        # helper function: get or create a team
        # def getCreateTeam(team)
        # print row['herculesnr'], row['lidsinds'], datetime.strptime(row['lidsinds'], "%Y-%m-%d")
        try:
            t = Team.objects.get(number=row['team_member'])
        except:
            t = Team.objects.create(number=row['team_member'], level=row['teamlevel']) # switchingdays=row['teamwisseldagen']

        #get or create pass
        try: 
            p = Pass.objects.get(knvbnr=row['Relatienr'])
        except:
            p = Pass.objects.create(knvbnr=row['Relatienr'], passtatus=row['passtatus']) # pasverloop=row['pasverloop'],

        #get or create hercules membeschnip info
        try:
            m = MembershipHercules.objects.get(herculesnr=row['Herculesnummer'])
        except:
            m = MembershipHercules.objects.create(herculesnr=row['Herculesnummer'], subscription=row['type_inschrijving'], injured=row['blessure'],  paid=row['betaald'])
            # try:
            #     m.enrolled=datetime.strptime(row['Lid sinds'], "%Y-%m-%d"), 
            # except:
            #     pass
            # try:
            #     m.membersince=datetime.strptime(row['Lid sinds'], "%Y-%m-%d")
            # except:
            #     pass

        # create player:
        addPlayer(row, knvbnr=p, herculesnr=m, team=t, user=row['user'])

    csvfile.close()

    # if User.objects.count() == 0:
    admin = User.objects.get(username='benteeuwen')
    # admin.set_password('geen')
    admin.is_superuser = True
    admin.is_staff = True
    admin.save()

    # add captains to teams
    for row in data:
        t = Team.objects.get(number=row['team'])
        p = Player.objects.get(knvbnr__knvbnr=row['captainknvbnr'])
        t.captain=p
        t.save()