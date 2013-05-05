import csv
from members.models import Player, Pass

with open('aanvoerders.csv', 'rU') as csvfile:

    data = csv.reader(csvfile, delimiter=';', dialect=csv.excel_tab)
    data.next()
    for row in data:
        print row
        print str(row[1])
        #pkpass = Pass.objects.get(knvbnr= str(row[1]))
        p1 = Player.objects.get(knvbnr__knvbnr = row[0])
        p1.captain = True
        p1.save()

    csvfile.close()
