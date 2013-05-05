from django import forms

class EditPlayerForm(forms.Form):
    # ATTACKER = 'Aanvaller'
    GOALY = 'Keeper'
    # DEFENDER = 'Verdediger'
    PLAYER = 'Speler'

    POSITION = (
    #     (ATTACKER, 'Aanvaller'),
    #     (DEFENDER, 'Verdediger'),
        (GOALY, 'Keeper'),
        (PLAYER, 'Speler'),
         )

    SUBSCRIBED ='Ingeschreven'
    UNSUBSCRIBED = 'Uitgeschreven'
    UNKNOWN = 'Onbekend'

    NIEUWSBRIEF = (
        (SUBSCRIBED, 'Ingeschreven'),
        (UNSUBSCRIBED, 'Uitgeschreven'),
        (UNKNOWN, 'Onbekend'),
        )

    first_name = forms.CharField(label = "Voornaam")
    suffix = forms.CharField(required=False, label = "Tussenvoegsel")
    last_name = forms.CharField(label="Achternaam")
    email = forms.EmailField(label='Email')
    role = forms.ChoiceField(label = "Positie", choices = POSITION, initial=PLAYER)
    #captain = forms.BooleanField(label="Aanvoerder",required=False)
    substitutewilling = forms.BooleanField(label="Wil invallen",required=False)
    nieuwsbrief = forms.ChoiceField(label = "Nieuwsbrief status", choices = NIEUWSBRIEF, initial=UNKNOWN)

class AddNewPlayerForm(forms.Form):
    first_name = forms.CharField(label = "Voornaam")
    suffix = forms.CharField(required=False, label = "Tussenvoegsel")
    last_name = forms.CharField(label="Achternaam")
    email = forms.EmailField(label='Email')
    # role = forms.ChoiceField(label = "Positie", choices = POSITION)
    mobile = forms.CharField(label = 'Telefoonnummer')

class ArrangeSubstitutesForm(forms.Form):
    substitutesneeded = forms.IntegerField(label = "Aantal invallers nodig")

class importMatchesForm(forms.Form):
     matches = forms.FileField(label = 'Sportlink wedstrijd CSV')

class importPlayersForm(forms.Form):
     playerszv = forms.FileField(label = 'Sportlink: zaalvoetballers')
     # playersall = forms.FileField(label = 'Sportlink: alle voetballers')
     # playersold = forms.FileField(label = 'Sportlink: gestopte voetballers')

class migrationForm(forms.Form):
    alldata = forms.FileField(label = 'Data spelers')
    teamcaptains = forms.FileField(label = 'Data team aanvoerders')