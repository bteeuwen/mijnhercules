from members.models import Player, Pass, MembershipHercules

mh = MembershipHercules.objects.all()
mhlist = []
for m in mh:
    mhlist.append(m)

pl = Player.objects.all()

for p in pl:
    mhlist.remove(p.herculesnr)

print mhlist