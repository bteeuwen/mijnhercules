from datetime import *

from django.db import models    
from django.contrib.auth.models import User
from django.db.models import Q

from members.models import Team, Player

class Location(models.Model):
    name = models.CharField(max_length=50)
    #city = models.CharField(max_length=50)
    #address = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name
    class Meta:
        ordering = ['name']


######################################### Models & managers relevant for matches ########################################################################

class TeamManager(models.Manager):
    def get_my_matches(self, myteampk):
        return self.filter(Q(teamhome__pk=myteampk) | Q(teamaway__pk=myteampk))

    def get_my_future_matches(self, myteampk):
        return self.exclude(date__lte=date.today()).filter(Q(teamhome__pk=myteampk) | Q(teamaway__pk=myteampk)).order_by('date')

    def get_subs_needed(self, gender):
        if gender == 'M':
            return Match.men.filter(Q(substitutesneeded_home__gte=1) | Q(substitutesneeded_away__gte=1)).exclude(date__lte=date.today()).order_by('date')
        elif gender == 'V':
            return Match.women.filter(Q(substitutesneeded_home__gte=1) | Q(substitutesneeded_away__gte=1)).exclude(date__lte=date.today()).order_by('date')

class FutureMatchManager(models.Manager):
    def get_query_set(self):
        #     matchessubsneeded = Match.objects.filter(number__icontains='VR').exclude(date__lte=date.today()).filter(substitutesneeded__gte=1)
        # matches = Match.objects.exclude(date__lte=date.today()).order_by('date').filter(Q(teamhome=team) | Q(teamaway=team))
        return super(FutureMatchManager, self).get_query_set().exclude(date__lte=date.today())

class FemaleMatchManager(models.Manager):
    def get_query_set(self):
        #     matchessubsneeded = Match.objects.filter(number__icontains='VR').exclude(date__lte=date.today()).filter(substitutesneeded__gte=1)
        # matches = Match.objects.exclude(date__lte=date.today()).order_by('date').filter(Q(teamhome=team) | Q(teamaway=team))
        return super(FemaleMatchManager, self).get_query_set().filter(Q(teamhome__number__icontains='Hercules VR') | Q(teamaway__number__icontains='Hercules VR'))

class MaleMatchManager(models.Manager):
    def get_query_set(self):
        #     matchessubsneeded = Match.objects.filter(number__icontains='VR').exclude(date__lte=date.today()).filter(substitutesneeded__gte=1)
        # matches = Match.objects.exclude(date__lte=date.today()).order_by('date').filter(Q(teamhome=team) | Q(teamaway=team))
        return super(MaleMatchManager, self).get_query_set().exclude(Q(teamhome__number__icontains='Hercules VR') | Q(teamaway__number__icontains='Hercules VR'))

class Match(models.Model):
    nrid = models.IntegerField(max_length=10)
    teamhome = models.ForeignKey(Team, related_name='match_teamhome')
    teamaway = models.ForeignKey(Team, related_name='match_teamaway')
    location = models.ForeignKey(Location)
    date = models.DateTimeField()

    substitutesneeded_home = models.IntegerField(max_length=2, blank=True, null=True)
    substituteoptions_home = models.ManyToManyField(Player, related_name='match_substituteoptions_home', blank=True, null=True)
    substitutes_home = models.ManyToManyField(Player,related_name='match_substitutes_home', blank=True, null=True)
    playerspresent_home = models.ManyToManyField(Player,related_name='match_playerspresenthome', blank=True, null=True)

    substitutesneeded_away = models.IntegerField(max_length=2, blank=True, null=True)
    substituteoptions_away = models.ManyToManyField(Player, related_name='match_substituteoptions_away', blank=True, null=True)
    substitutes_away = models.ManyToManyField(Player,related_name='match_substitutes_away', blank=True, null=True)    
    playerspresent_away = models.ManyToManyField(Player,related_name='match_playerspresentaway', blank=True, null=True)
    
    def setSubstitutes(self, team, amountsubsneeded):
        if team == self.teamhome.pk:
            self.substitutesneeded_home = amountsubsneeded
        elif team == self.teamaway.pk:
            self.substitutesneeded_away = amountsubsneeded

    def addSubstitute(self, teampk, player):
        if int(teampk) == self.teamhome.pk:
            self.substituteoptions_home.add(player)
        elif int(teampk) == self.teamaway.pk:
            self.substituteoptions_away.add(player)
        # raise ValueError

    def removeSubstitute(self, teampk, player):
        if int(teampk) == self.teamhome.pk:
            self.substituteoptions_home.remove(player)
        elif int(teampk) == self.teamaway.pk:
            self.substituteoptions_away.remove(player)
        # raise ValueError

    def getSubstitutes(self, teampk):
        if int(teampk) == self.teamhome.pk:
            if self.substituteoptions_home.all():
                return self.substituteoptions_home.all()
            else:
                return 0
        elif int(teampk) == self.teamaway.pk:
            if self.substituteoptions_away.all():
                return self.substituteoptions_away.all()
            else:
                return 0

    def playerPresent(self, teampk, player):
        if int(teampk) == self.teamhome.pk:
            if player in self.playerspresent_home.all():
                return True
            else:
                return False
        elif int(teampk) == self.teamaway.pk:
            if player in self.playerspresent_away.all():
                return True
            else:
                return False

    def addMatchPresence(self, teampk, player):
        if int(teampk) == self.teamhome.pk:
            self.playerspresent_home.add(player)
        elif int(teampk) == self.teamaway.pk:
            self.playerspresent_away.add(player)
        # raise ValueError

    def removeMatchPresence(self, teampk, player):
        if int(teampk) == self.teamhome.pk:
            self.playerspresent_home.remove(player)
        elif int(teampk) == self.teamaway.pk:
            self.playerspresent_away.remove(player)
        # raise ValueError

    def getPresentPlayers(self, teampk):
        if int(teampk) == self.teamhome.pk:
            if self.playerspresent_home.all():
                return self.playerspresent_home.all()
            else:
                return 0
        elif int(teampk) == self.teamaway.pk:
            if self.playerspresent_away.all():
                return self.playerspresent_away.all()
            else:
                return 0

    def getSubstitutesNeeded(self, team):
        if team == self.teamhome.pk:
            return self.substitutesneeded_home
        elif team == self.teamaway.pk:
            return self.substitutesneeded_away

    def _getNrSubstitutesNeeded(self):
        subs = 0
        if self.substitutesneeded_away != None:
            subs += self.substitutesneeded_away
        if self.substitutesneeded_home != None:
            subs += self.substitutesneeded_home
        return subs
    substitutesneeded = property(_getNrSubstitutesNeeded)

    objects = TeamManager() # The default manager.
    # participants = models.ManyToManyField(Player,related_name='match_participants', blank=True, null=True)
    # absentees = models.ManyToManyField(Player,related_name='match_absentees', blank=True, null=True)
    women = FemaleMatchManager()
    men = MaleMatchManager()
    futurematches = FutureMatchManager()

    # def femaleMatch(self):
    #   if 'VR' in self.teamhome.number or 'VR' in self.teamaway.number:
    #       return True
    #   else:
    #       return False
    def isTeam(self, teampk):
        if self.teamaway.pk == teampk or self.teamhome.pk == teampk:
            return True
        else:
            return False

    def getHercules(self):
        teams = []
        if 'Hercules' in self.teamhome.number:
            teams.append(self.teamhome)
        if 'Hercules' in self.teamaway.number:
            teams.append(self.teamaway)
        return teams


    # omgaan met 2 hercules teams tegen elkaar
    # type wedstrijd; oefen, competitie, beker

    # tegenstander?
    # def _get_my_opponent(self,):
    #     "Returns the team's opponent."
    #     if self.teamhome == team:
    #         return u'%s' % self.teamaway
    #     elif 'Hercules' in self.teamaway:
    #         return u'%s' % self.teamhome
    # name = property(_get_name)

    def __unicode__(self):
        return "%s - %s (%s)" % (self.teamhome, self.teamaway, self.date.strftime("%d %B %H:%M"))
    class Meta:
        ordering = ['-date']

##################################################################################################################################################################