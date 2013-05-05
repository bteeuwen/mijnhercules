from datetime import *
from matches.models import Match
from django.template import RequestContext
from django.shortcuts import render_to_response, render
from django.contrib.auth.models import User
from django.db.models import Q

#### TODO:
## spelers die op pas wachten tonen.
## spelers laten kiezen wiens pas gearriveerd is om hen + hun aanvoerders in cc te mailen. 

## wanbetalers lijst tonen.
## comment toevoegen om update over actie naar wanbetaler.

## geblesseerden tonen.

## degenen die half jaar betalen afvinken als ze hun pas hebben ingeleverd.

# def home(request):
# 	if request.user.is_authenticated() & request.user.is_active:
# 		u1 = User.objects.get(username=request.user.username)
# 		team = u1.get_profile().team_member
# 		name = '%s %s %s' % (u1.get_profile().first_name, u1.get_profile().suffix, u1.get_profile().last_name)
# 		count = Player.objects.count()
# 		pas = u1.get_profile().knvbnr
# 		pasverloop = pas.pasverloop
# 		matches = Match.objects.filter(Q(teamhome=team) | Q(teamaway=team))
# 		p = Player.objects.filter(team_member=team)
# 		return render(request, 'base.html', {'name': name, 'team': team, 'aantalspelers': count, 'team_detail': team, 'player_list': p, 'pasverloop': pasverloop, 'matches': matches})
# 	return render_to_response('base.html',
# 		context_instance=RequestContext(request))

def home(request):
    matches = Match.futurematches.all()
    return render(request, "base.html", {'allmatches':matches})