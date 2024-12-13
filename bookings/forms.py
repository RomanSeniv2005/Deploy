from django import forms

class RouteForm(forms.Form):
    departure = forms.CharField(label="Звідки", max_length=100)
    destination = forms.CharField(label="Куди", max_length=100)
    date = forms.DateField(label="Дата", widget=forms.SelectDateWidget)
