from datetime import *
import csv
from sys import argv
from members.models import Player, Team, Location, Match
from members.views import addPlayer
import re
from pytz import timezone
import pytz

eu = pytz.utc
# eu = timezone('Europe/Amsterdam')

#import ims

script, first = argv

def saveMatch(m, date, t1, t2, location):
    m.date = datetime.strptime((date), '%d %b %Y %H:%M')
    m.teamhome = t1
    m.teamaway = t2
    m.location = location
    m.save()

with open(first, 'rU') as csvfile:
    data = csv.reader(csvfile, delimiter=';', dialect=csv.excel_tab)
    data.next()
    for row in data:
        if "Mannen Zaal" in row[3]:
        #print row
            # l = Location.objects.all()
            # l.delete()
            
            # add locations if not yet existent in the db
            try:
                loc = re.match(r'(.*)\sveld', row[7])
                loc = loc.group(1)
                loc = Location.objects.get(name=loc)
                #print "Existing", loc
            except:
                loc = re.match(r'(.*)\sveld', row[7])
                loc = Location.objects.create(name=loc.group(1))
                loc.save()

            # add team if not yet existent in the db
            try:
                t1 = Team.objects.get(number=row[4])
            except:
                t1 = Team.objects.create(number = row[4], level = '99')
                t1.save()
            try:
                t2 = Team.objects.get(number=row[5])
            except:
                t2 = Team.objects.create(number = row[5], level = '99')
                t2.save()
            try:
                m = Match.objects.get(nrid=row[0])
                # print "got %s" % m
                m.date = eu.localize(datetime.strptime((row[1]+" " + row[2]), '%d-%m-%y %H:%M'))
                m.teamhome = t1
                m.teamaway = t2
                m.location = loc
                m.save()
                #print m
                # saveMatch(m, row[1] + row[2], t1, t2, loc)
            except:
                #print "except match with %s and %s" % (t1, t2)
                m = Match(
                    nrid=row[0], 
                    date = eu.localize(datetime.strptime((row[1]+" " + row[2]), '%d-%m-%y %H:%M')),
                    teamhome = t1,
                    teamaway = t2,
                    location = loc)
                m.save()
    csvfile.close()