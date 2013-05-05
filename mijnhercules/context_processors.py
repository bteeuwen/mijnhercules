from datetime import *

from django.template import RequestContext
from django.shortcuts import render_to_response, render
from django.contrib.auth.models import User
from django.db.models import Q

from members.models import Team, Player
from matches.models import Match

def playerContext(request):
    player, name, team, count, team, p, pasverloop = [],[],[],0,[],[],[]
    matches = Match.futurematches.all()
    try:
        if request.user.is_authenticated() & request.user.is_active:
            player = request.user.player
            count = Player.objects.count()
            matches = Match.objects.get_my_future_matches(player.team_member.pk)
            p = Player.objects.filter(team_member=player.team_member)
    except:
        pass
    # else:
    return {'player': player,'aantalspelers': count,'player_list': p,'matches': matches}

def substitutesNeeded(request):
    # TO DO: model def to return female matches
    matchessubsneeded = []
    try:    
        if request.user.is_authenticated() & request.user.is_active:
            player = request.user.player
            matchessubsneeded = Match.objects.get_subs_needed(player.gender)
    except:
        pass    
    return {'matchessubsneeded': matchessubsneeded}