from datetime import *

from django.db import models    
from django.contrib.auth.models import User
from django.db.models import Q
from django.conf import settings

######################################### Models & managers relevant for TEAMS ########################################################################


class FemaleTeamManager(models.Manager):
    def get_query_set(self):
        return super(FemaleTeamManager, self).get_query_set().filter(number__icontains='Hercules VR')

class MaleTeamManager(models.Manager):
    def get_query_set(self):
        return super(MaleTeamManager, self).get_query_set().filter(number__icontains='Hercules').exclude(number__icontains='VR')

class HerculesTeamsManager(models.Manager):
    def get_query_set(self):
        return super(HerculesTeamsManager, self).get_query_set().filter(number__icontains='Hercules')

class Team(models.Model):
    number = models.CharField(max_length=40)
    level = models.IntegerField(max_length=2)
    switchingdays = models.IntegerField(max_length=2, null=True, blank=True)
    captain = models.ForeignKey('Player', blank=True, null=True)
    
    objects = models.Manager() # The default manager.
    herculesteams = HerculesTeamsManager()
    women = FemaleTeamManager()
    men = MaleTeamManager()
    
    def __unicode__(self):
        return self.number

    class Meta:
        ordering = ['number']

##################################################################################################################################################################


class MembershipHercules(models.Model):
    # define subscription types:
    YEAR = 'Jaar'
    FALL =  'Herst'
    SPRING = 'Lente'
    NONE = 'Wachtlijst'
    MEMBERSHIP_CHOICES = (
        (YEAR, 'Volledig jaar'),
        (FALL, 'Half jaar (aug/dec)'),
        (SPRING, 'Half jaar (jan-jun)'),
        (NONE, 'Nog niet ingedeeld'),
        )
    herculesnr = models.CharField(max_length=10, null=True, blank=True, unique=True)
    subscription = models.CharField(max_length=24, choices=MEMBERSHIP_CHOICES, default = NONE)
    injured = models.NullBooleanField(blank=True)
    enrolled = models.DateField(null=True, blank=True)
    membersince = models.DateField(null=True, blank=True)
    soccer = models.NullBooleanField(blank=True)
    paid = models.NullBooleanField(blank=True)

    def __unicode__(self):
        return self.herculesnr
    class Meta:
        ordering = ['herculesnr']

class Pass(models.Model):
    # define pass delivery stages:
    PICTURE = 'Foto'
    BAR_T = "Bar (tijdelijk)"
    PLAYER_T = "Speler (tijdelijk)"
    PRINTSHOP = 'Drukkerij'
    BAR = "Bar"
    PLAYER = "Speler heeft spelerspas"
    WITHDRAWN = "Ingenomen"

    PASS_STATUS = (
        (PICTURE, 'Foto opsturen'),
        (BAR_T, "Bar (tijdelijk)"),
        (PLAYER_T, "Speler heeft tijdelijk pas"),
        (PRINTSHOP, 'Drukkerij bezig'),
        (BAR, "Def. pas achter bar"),
        (PLAYER, "Speler heeft spelerspas"),
        (WITHDRAWN, "Ingenomen"),
        )

    knvbnr = models.CharField(max_length=10, null=True, blank=True, unique=True)
    pasverloop = models.DateField(null=True, blank=True)
    passtatus = models.CharField(choices=PASS_STATUS, default = PICTURE, null=True, blank=True, max_length=100)

    def __unicode__(self):
        return self.knvbnr
    class Meta:
        ordering = ['knvbnr']

######################################### Models & managers relevant for players ########################################################################

class MaleManager(models.Manager):
    def get_query_set(self):
        return super(MaleManager, self).get_query_set().filter(gender='M')

class FemaleManager(models.Manager):
    def get_query_set(self):
        return super(FemaleManager, self).get_query_set().filter(gender='V')

class Player(models.Model):
    # ATTACKER = 'Aanvaller'
    GOALY = 'Keeper'
    # DEFENDER = 'Verdediger'
    # ALLROUNDER = 'Speler'
    PLAYER = 'Speler'

    POSITION = (
        (PLAYER, 'Speler'),
        (GOALY, 'Keeper'),
        )
    # player relations to other models:
    knvbnr = models.OneToOneField(Pass, null=True, blank=True)
    herculesnr = models.OneToOneField(MembershipHercules, null=True, blank=True)
    team_member = models.ForeignKey(Team, null=True, blank=True)
    
    # user auth django 1.4:
    # user=models.OneToOneField(User,unique=True, null=True, blank=True)
    # user auth django 1.5:
    user=models.OneToOneField(settings.AUTH_USER_MODEL)

    # name:
    first_name = models.CharField(max_length=30, null=True, blank=True)
    suffix = models.CharField(max_length=10, null=True, blank=True)
    last_name = models.CharField(max_length=30, null=True, blank=True)
    
    gender = models.CharField(max_length=1, null=True, blank=True)
    age = models.DateField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    cellphone = models.CharField(max_length=15, null=True, blank=True)
    regularphone = models.CharField(max_length=14, null=True, blank=True)
    
    # address
    postalcode = models.CharField(max_length=8, null=True, blank=True)
    city = models.CharField(max_length=51)
    street = models.CharField(max_length=55, null=True, blank=True)
    streetnr = models.IntegerField(null=True, blank=True)
    streetnrplus = models.CharField(max_length=10, null=True, blank=True)
    
    # is player a keeper or field player?
    role = models.CharField(choices=POSITION, default =PLAYER, max_length=20,null=True, blank=True)
    
    # does player want to substitute for other teams' matches?
    substitutewilling = models.NullBooleanField(blank=True, null=True)
    
    objects = models.Manager() # The default manager.    
    men = MaleManager()
    women = FemaleManager()

    # guardian permissions
    # class Meta:
    #     ordering = ['last_name']
    #     permissions = (
    #         ('view_player', 'View player'),
    #         ('edit_player', 'Edit player'),
    #     )

    def _get_full_name(self):
        "Returns the person's full name."
        if self.suffix:
            return u'%s %s %s' % (self.first_name, self.suffix, self.last_name)
        return u'%s %s' % (self.first_name, self.last_name)
    full_name = property(_get_full_name)

    def is_Female(self):
        return self.gender == 'V'

    def is_Male(self):
        return self.gender == 'M'
    
    def __unicode__(self):
        if self.suffix:
            return u'%s %s %s' % (self.first_name, self.suffix, self.last_name)
        return u'%s %s' % (self.first_name, self.last_name)

