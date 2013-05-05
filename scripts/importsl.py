from datetime import *
import csv
from sys import argv
from members.models import Player, Pass, MembershipHercules
from members.views import addPlayer
import re
#import ims

script, first, second, third = argv

## OPEN: hoe omgaan met adres wijzigingen?

#def SportlinkSynch(file1, file2, file3):
# haal bestaande knvb & hercules nr's op uit mh
mhpasses = Pass.objects.all()
mhpasnrs = []
for m in mhpasses:
    mhpasnrs.append(m.knvbnr)

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
    result = "%s %s %s %s %s" % (z[0], z[1], z[2], z[3],z[9])
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
with open(first, 'rU') as csvfile:
    data = csv.reader(csvfile, delimiter=';', dialect=csv.excel_tab)
    data.next()
    for row in data:
        zaalvoetballers.append(row)
        zvpas.append(row[0])
        zvherculesnr.append(row[9])

    csvfile.close()

# open bestand met alle voetballers
voetballers = []
vpas = []
with open(second, 'rU') as csvfile:
    data = csv.reader(csvfile, delimiter=';', dialect=csv.excel_tab)
    data.next()
    for row in data:
        voetballers.append(row)
        vpas.append(row[0])
    csvfile.close()

# open bestand met alle gestopte voetballers
stoppers = []
stpas = []

with open(third, 'rU') as csvfile:
    data = csv.reader(csvfile, delimiter=';', dialect=csv.excel_tab)
    data.next()
    for row in data:
        stoppers.append(row)
        stpas.append(row[0])
    csvfile.close()

# sla alle hercules nummers op die in mh staan
mislukt = {}
gelukt = {}
cases = [   'Hercules nummers toevoegen aan MijnHercules',
            'Hercules nummers teveel in MijnHercules',
            'KNVB nummers teveel in MijnHercules',
            'KNVB voor-inschrijving nieuwe speler (tijdelijk knvb relatienummer)', 
            'KNVB voor-inschrijving nieuwe speler updaten met definitief knvb relatienummer', 
            'KNVB definitieve inschrijving nieuwe speler', 
            'Uitschrijving speler bij Hercules (zowel veld als zaal)', 
            'Uitschrijving speler bij Hercules (alleen in zaal)',
            'Uitschrijving anders?']
for c in cases:
    gelukt[c] = []
    mislukt[c] = []

# loop alle hercules nummers na
for z in zaalvoetballers:
    # indien nieuw
    if z[9] != '' and z[9] not in mhherculesnrs:
        # voeg toe aan mh
        h = MembershipHercules(herculesnr = str(z[9])) 
        h.save()
        gelukt['Hercules nummers toevoegen aan MijnHercules'].append(reportPlayer(z))
    # als er geen hercules nummer bekend is:
    elif z[9] == '':
        # tel
        # rapporteer zodat Marianne kan bijwerken
        #misser = "%s %s %s %s %s" % (z[0], z[1], z[2], z[3], z[9])
        mislukt['Hercules nummers toevoegen aan MijnHercules'].append(reportPlayer(z))

# loop alle knvb nummers na
# voor ieder sl knvb nr:
for v in zaalvoetballers:
    
    if v[0] not in mhpasnrs:
        #print "Nieuw!: %s" % v
        #print str(v[1]) + str(v[3]) in mhplayernames
        
        # indien nieuw (5 tot 7 getallen)
        if re.search("(\d{5,7})", v[0]):
            #print "Pre-inschrijving: %s" % v
            # Controleer dubbele inschrijving in SL:
            for y in zaalvoetballers:
                if (y[1] + y[2] + y[3] + y[4]) == (v[1] + v[2] + v[3] + v[4]) and y[0] != v[0]:
                    #print "Matches with: %s" % y
                    mislukt['KNVB voor-inschrijving nieuwe speler (tijdelijk knvb relatienummer)'].append(reportPlayer(y))        

            #print "Nog niet bekende voorinschrijving"
            # voeg toe aan mh
            addPlayer(v)
            gelukt['KNVB voor-inschrijving nieuwe speler (tijdelijk knvb relatienummer)'].append(reportPlayer(v))
        else:
            # controleer of er een tijdelijke inschrijving in MH staat op basis van voor- en achternaam.
            if (str(v[1]) + str(v[3])) in mhplayernames:
                #print "Updating tijdelijke inschrijvingsnummer met definitieve nummer:"
                p1 = Player.objects.get(first_name=str(v[1]), last_name=str(v[3]))
                pasnr = p1.knvbnr
                pkpass = Pass.objects.create(knvbnr=str(row[0]))
                p1.knvbnr = pkpass 
                addPlayer(v)
                gelukt['KNVB voor-inschrijving nieuwe speler updaten met definitief knvb relatienummer'].append(reportPlayer(v))

            else:
                #print "Nog niet bekende definitieve inschrijving: %s" % v
                # voeg toe aan mh
                addPlayer(v)
                gelukt['KNVB definitieve inschrijving nieuwe speler'].append(reportPlayer(v))
    elif v[0] in mhpasnrs:
        #print v[0]
        pasnr = Pass.objects.get(knvbnr=str(v[0]))
        p1 = Player.objects.get(knvbnr=pasnr)
        #print pasnr

        ## update hercules number if current player in MH has none:
        if p1.herculesnr == None and v[9] != '':
            #print "Player %s with nr %s has the nr %s in the import" % (p1, p1.herculesnr, v[9])
            hnr = MembershipHercules.objects.get(herculesnr = str(v[9]))
            #print hnr
            p1.herculesnr = hnr
            p1.save()

        ## update whether player is playing in the field as well
        if 'Veld' in str(v[17]):
            try:
                #print 'voetballer %s' % v
                herc = MembershipHercules.objects.get(herculesnr = str(v[9]))
                herc.soccer = True
                herc.save()
            except:
                pass
        elif 'Veld' not in str(v[17]):            
            try:
                #print 'zaalvoetballer %s' % v
                herc = MembershipHercules.objects.get(herculesnr = str(v[9]))
                herc.soccer = False
                herc.save()
            except:
                pass

# Gestopte spelers op non-actief plaatsen.
for mv in mhpasnrs:
    if mv in stpas:
        #print "%s Quit." % mv
        try:
            p1 = Player.objects.get(knvbnr__knvbnr=mv)
            p1.delete()
        except:
            pass
        mhpas = Pass.objects.get(knvbnr=mv)
        mhpas.delete()
        # p1.active = False
        # p1.save()
        gelukt['Uitschrijving speler bij Hercules (zowel veld als zaal)'].append(p1)
    elif (mv not in zvpas) and (mv in vpas):
        #print "%s Quit futsal, but still playing in the field." % mv
        try:
            p1 = Player.objects.get(knvbnr__knvbnr=mv)
            p1.delete()
        except:
            pass
        mhpas = Pass.objects.get(knvbnr=mv)
        mhpas.delete()
        # p1.active = False
        # p1.save()
        gelukt['Uitschrijving speler bij Hercules (alleen in zaal)'].append(p1)
    elif mv in zvpas:
        pass
    else:
        print "Weird: %s" % mv
        mislukt['Uitschrijving anders?'].append(mv)
mhpasses = Pass.objects.all()
mhpasnrs = []
for m in mhpasses:
    mhpasnrs.append(m.knvbnr)

mhherculesmem = MembershipHercules.objects.all()
mhherculesnrs = []
for m in mhherculesmem:
    mhherculesnrs.append(m.herculesnr)

for h in mhherculesnrs:
    if h not in zvherculesnr:
        #print h
        try:
            p = Player.objects.get(MembershipHercules__herculesnr=h)
            print p
        except:
            #print "no one found"
            MembershipHercules.objects.get(herculesnr = h).delete()
            gelukt['Hercules nummers teveel in MijnHercules'].append(h)

for h in mhpasnrs:
    if h not in zvpas:
        #print h
        try:
            p = Player.objects.get(knvbnr__knvbnr=h)
            print p
        except:
            #print "no one found"
            Pass.objects.get(knvbnr=h).delete()
            gelukt['KNVB nummers teveel in MijnHercules'].append(h)

## Saving a log:
filename = 'logs/sportlink_sync_' + timestamp() + ".txt"
out_file = open(filename, "w")
out_file.write("--- SUCCEEDED ----\n")

# print "--- Gelukt ---"
# for k,v in gelukt.iteritems():
#     print k, v
# print "--- Mislukt ---"
# for k,v in mislukt.iteritems():
#     print k, v

for k,val in gelukt.iteritems():
    #print k
    out_file.write(" *** " + k + "\n")
    for v in val:
        out_file.write(str(v) + "\n")
    out_file.write("\n\n")

out_file.write("\n")

out_file.write("--- FAILED ----\n")
for k,val in mislukt.iteritems():    
    #print k
    out_file.write(" *** " + k + "\n")
    for v in val:
        out_file.write(str(v) + "\n")
    out_file.write("\n\n")
out_file.close()

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
            # als spelactiviteit op 't veld is gewijzigd
                # update veld spelactiviteit

# voor alle knvb nummers in mh:
    # als niet in SL bestand:
        # als in sl oud leden bestand:
            # zet speler op non-actief 
            # tel als uitschrijving
        # als wel in sl alle leden bestand, maar zonder zaal spelactiviteit
            # zet speler op non-actief
            # tel als gestopt met zaalvoetbal
        # rapporteer als afwijking
