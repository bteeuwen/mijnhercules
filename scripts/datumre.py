from members.models import Player, Pass, MembershipHercules
from datetime import *
import csv

# datum= "BBSJ118;Anita;;Stalenhoef;V;12-02-65;;030-2710440;;5942;NIEUWEGEIN;Strawinskystraat;80;;3438 XR;22-07-97;22-07-97;Zaal -  Week"

# #print datum
# datummatch = re.search(r';(\d{2})-(\d{2})-(\d{2});', datum, flags=0)
# #datummatch = re.search(pattern, datum1, flags=0)
# print datummatch.group(1)
# print datummatch.group(2)
# print datummatch.group(3)

# datum1 = "22-07-97"

# 

with open('130117sl.csv', 'rU') as csvfile:
    data = csv.reader(csvfile, delimiter=';', dialect=csv.excel_tab)
    data.next()
    for row in data:
        p1 = Player.objects.get(knvbnr__knvbnr = row[0])
        p1.age = datetime.strptime(str(row[5]), "%d-%m-%y")
        p1.save()
        try:
            herc = MembershipHercules.objects.get(herculesnr = str(row[9]))
            print herc
            herc.membersince = datetime.strptime(str(row[16]), "%d-%m-%y")
            print herc.membersince
            herc.enrolled = datetime.strptime(str(row[15]), "%d-%m-%y")
            herc.save()
        except:
            pass
    csvfile.close()