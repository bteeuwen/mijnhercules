import re
import csv
import cStringIO
from members.models import *
import pytz
from datetime import *
from sys import argv

#unpack those cli arguments
script, filename = argv


eu = pytz.utc
csvfile = open(filename, 'rU')

data = csvfile.read()
reader = csv.reader(cStringIO.StringIO(data), delimiter=';')

try:
    assert 'Wedstrijdnummer' and 'Wedstrijddatum (niet geformatteerd)' and 'Aanvangstijd' and 'Aanduiding' and \
    'Thuis team' and 'Uit team' and 'Sport omschrijving' and 'Veld' and 'Accommodatie naam' and 'Plaats' in reader.next()
except:
    print 'not good'

csvfile.seek(0)
reader = csv.DictReader(cStringIO.StringIO(data), delimiter=';')

dates = []
for row in reader:
    try:
        date = eu.localize(datetime.strptime((row['Wedstrijddatum (niet geformatteerd)']+" " + row['Aanvangstijd']), '%d-%m-%y %H:%M'))
    except:
        date = eu.localize(datetime.strptime((row['Wedstrijddatum (niet geformatteerd)']+" " + row['Aanvangstijd']), '%d-%m-%Y %H:%M'))
    dates.append(date)

mindate = min(dates)
maxdate = max(dates)

existingmatches = Match.objects.filter(date__lte=maxdate).filter(date__gte=mindate)

# for e in existingmatches:
#     print e

csvfile.seek(0)
reader = csv.DictReader(cStringIO.StringIO(data), delimiter=';')
savedmatches=[]
for row in reader:
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

for e in existingmatches:
    if e not in savedmatches:
        e.delete()

print savedmatches