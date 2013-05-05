from django import forms


PRESENCE_OPTIONS = (
    ('PRESENT', 'Aanwezig'),
    ('ABSENT', 'Afwezig'),
    ('MAYBE', 'Misschien'),
)

class MatchPresence(forms.Form):
    presence = forms.ChoiceField(choices=PRESENCE_OPTIONS)


class ArrangeSubstitutesForm(forms.Form):
    substitutesneeded = forms.IntegerField(label = "Aantal invallers nodig")

class importMatchesForm(forms.Form):
     matches = forms.FileField(label = 'Sportlink wedstrijd CSV')
