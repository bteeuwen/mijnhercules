# import requests
from datetime import *
# r = requests.get('http://senioren.voetbal.nl/')
# print r.text
import re
from bs4 import BeautifulSoup

## TO DO:
# request post login 
import urllib2
import urllib

# The URL to this service
# URL = 'http://senioren.voetbal.nl/'

# def main():
#     # Here is the data that FireBug said we sent
#     postdict = {

#                     'form_build_id' : 'form-07dc32d6ac33a49423813ea266ee4282'
#                 'form_id' : 'login_block_v3_login_menu_form'
#                 'name':    'bteeuwen'
#                 'op' : 'Inloggen'
#                 'pass' :   'G33Nvoetbal'

#     'city' : 'San Francisco',
#                 'demotype' : 'actual',
#                 'state' : 'CA',
#                 'voice' : 'David',
#                 'submit':'Synthesize the weather'}

#     # Encode it into HTTP form, blah de blah blah
#     postme = urllib.urlencode(postdict)

#     # Send it...
#     fd = urllib2.urlopen(URL, postme)
#     return fd


# scale up multiple teams

# parse data
class Match(object):
    def __init__(self, date, t_home, t_away, accommodation):
        self.date = datetime.strptime(("2013 " + date), '%Y %d %b, %H:%M')
        #self.players = players
        self.t_away = t_away
        self.t_home = t_home
        self.accommodation = accommodation
    def returnPlayers(self):
        return self.players
    def returnHomeTeam(self):
        return self.t_home
    def returnAwayTeam(self):
        return self.t_away
    def returnDate(self):
        return self.date
    def returnAccommodation(self):
        return self.accommodation

soup = BeautifulSoup(open('H17.htm'))
matchviews = soup.find_all('div', class_='mijn-teams-programma-row mijn-teams-periode-programma-blok ')
matches = matchviews[1].find_all('div', class_= "mijn-teams-programma-row-detail")

games = []
for m in matches:
    date = m.find('div', 'datum-tijd meer-info-click').string.strip()
    accommodatie = m.find('div', 'accommodatie meer-info-click').string.strip()
    players = m.find('div', 'wedstrijd meer-info-click').get_text(strip=True)
    players = players.split("-")
    plhome = re.match( r'(.*)[(]', players[0])
    plaway = re.match(r'\s+(\w+.*)[(]', players[1])
    games.append(Match(date, plhome.group(1).strip(), plaway.group(1).strip(), accommodatie))

for g in games:
    #if "Hercules" in g.returnAwayTeam() or "Hercules" in g.returnHomeTeam():
    print g.returnDate(), g.returnHomeTeam(), g.returnAwayTeam()