Herculesnummer,type_inschrijving,blessure,Lid sinds,Registratiedatum,betaald,Relatienr,pasverloop,passtatus,team_member,teamlevel,teamwisseldagen, teamaanvoerder,user,Roepnaam,Tussenvoegsels,Achternaam,Geslacht,Geb datum,E-mail,Mobiel,Telefoon,Postcode,Woonplaats,Straat,Huisnr,Huisnr toev,role,substitutewilling


# date strftime!!!
# try:
#         geboortedatum = datetime.strftime(p.age, "%d-%m-%y")
#     except:
#         geboortedatum = None
from members.models import *

for p in Player.objects.all():
    
    print str(p.herculesnr) + "," + str(p.herculesnr.subscription) + "," + str(p.herculesnr.injured) + "," + str(p.herculesnr.enrolled) + "," + str(p.herculesnr.membersince)+ "," + str(p.herculesnr.paid)+ "," +  str(p.knvbnr) + "," + str(p.knvbnr.pasverloop) +","+ str(p.knvbnr.passtatus)+","+ str(p.team_member) + "," + str(p.team_member.level) + "," + str(p.team_member.switchingdays) + "," + str(p.team_member.captain) + "," + str(p.user) + "," + p.first_name + "," +  p.suffix + "," +  p.last_name + "," + str(p.gender) + "," + datetime.strftime(p.age, "%d-%m-%y") + "," + str(p.email) + "," + str(p.cellphone) + "," + str(p.regularphone) + "," + str(p.postalcode) + "," + str(p.city) + "," + str(p.street) + "," + str(p.streetnr) + "," +  str(p.streetnrplus) + "," + str(p.role) + "," + str(p.substitutewilling)

team,captain

for t in Team.objects.all():
    try:
        print str(t.number) + "," + str(t.captain.knvbnr)
    except:
        pass