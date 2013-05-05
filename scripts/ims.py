import sys
import csv
from members.models import Team, Player, Pass, MembershipHercules
from django.contrib.auth.models import User
from guardian.shortcuts import assign

#### TODO:
## sportlink nieuw bestand nieuwste spelers importeren.
# reguliere expressie om data om te draaien veranderen.

## aanvoerders rechten geven om teamgenoten aan te passen.

# spelers recht geven eigen gegevens aanpassen.

# eerst de teams invoeren.

def ImportTeams():
	t = Team.objects.all()
	t.delete()
	with open('teams.txt', 'rb') as csvfile:
		data = csv.reader(csvfile, delimiter=',')
		for row in data:
			t1 = Team(number=str(row[0]), level = int(row[1]))
			t1.save()
	csvfile.close()

def ImportPass():
	k = Pass.objects.all()
	k.delete()
	with open('knvbnr.txt', 'rb') as csvfile:
		data = csv.reader(csvfile, delimiter=',')
		for row in data:
			p = Pass(knvbnr=str(row[0]))
			p.save()
	csvfile.close

def ImportHercules():
	h = MembershipHercules.objects.all()
	h.delete()
	with open('herculesnr.txt', 'rU') as csvfile:
		data = csv.reader(csvfile, delimiter=',')
		for row in data:
			p = MembershipHercules(herculesnr=str(row[0]))
			p.save()
	csvfile.close

# dan de spelers.
def ImportPlayers():
	# de boel eerst leeggooien.
	p = Player.objects.all()
	p.delete()
	u = User.objects.all().exclude(id=1)
	u.delete()
	with open('spelers.txt', 'rb') as csvfile:
		data = csv.reader(csvfile, delimiter=',')
		success = 0
		failed = 0
		p1 = Player.objects.all()
		for row in data:
			#print row
			try:
				pkpass = Pass.objects.get(knvbnr=str(row[3]))
				#print str(row[15])
				teampk = Team.objects.get(number=str(row[15]))
				#print teampk
			except:
				print "pkpass for %s failed" % row
			p1 = Player(
				first_name=str(row[0]),
				suffix=str(row[1]),
				last_name=str(row[2]),
				knvbnr=pkpass,
				#herculesnr=herculespk, 
				#membersince=str(row[16]),				
				gender=str(row[5]),
				#age=str(row[5]),
				email=str(row[6]),
				cellphone=str(row[7]),
				regularphone=str(row[8]),
				postalcode=str(row[9]),
				street=str(row[10]),
				streetnr=str(row[11]),
				streetnrplus=str(row[12]),
				city=str(row[13]),
				role=str(row[14]),
				team_member=teampk)
				#enrolled=str(row[15]))
			p1.save()
			try:
				herculespk = MembershipHercules.objects.get(herculesnr=str(row[4]))
				#print teampk
				p1.herculesnr=herculespk
				p1.save()
			except:
				print "hercules nr for %s failed with nr %s" % (row, str(row[4]))
				pass
			success += 1
			if str(row[0]) and str(row[2]):
					account = User.objects.create(username=((str(row[0]) + str(row[2])).lower().replace(" ", "")))
					p1.user = account
					account.email= str(row[6])
					p1.save()
					account.save()
		print success
	csvfile.close()

## aanvoerders rechten geven om teamgenoten aan te passen.
# get all captains
	# for every captain
		# get all players that captain is captain off.
		# assign edit right for captain over all his/her players.

def editRights():	
	captains = User.objects.filter(player__role='Aanvoerder')
	for c in captains:
		#print c
		team = c.get_profile().team_member
		teamplayers = Player.objects.filter(team_member=team)
		#print teamplayers
		for t in teamplayers:
			assign('edit_player', c, t)
		#for t in teamplayers:
		#	print c.has_perm('edit_player', t)

# def ImportPasverlopen():
# 	with open('pasverlopen.csv', 'U') as csvfile:
# 		data = csv.reader(csvfile, delimiter=';')
# 		success = 0
# 		failed = 0
# 		for row in data:
# 			try:
# 				p1 = Pass.objects.get(knvbnr=str(row[0]))
# 				p1.pasverloop = str(row[2])
# 				p1.passtatus = str(row[3])
# 				p1.save()
# 				success = success + 1
# 			except:
# 				failed = failed + 1
# 		print "%s pasverlopen succeeded, %s failed." % (success, failed)
# 	csvfile.close()

print "strating teams"
ImportTeams()
print "strating passes"
ImportPass()
print "strating herculesnr"
ImportHercules()
print "strating players"
ImportPlayers()
# print "Starting assigning edit rights to captains and teamplayers"
# editRights()
#ImportPasverlopen()