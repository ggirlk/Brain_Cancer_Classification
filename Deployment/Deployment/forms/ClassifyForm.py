from django import forms


class ClassifyForm(forms.Form):
    #name = forms.CharField()
    imgfield = forms.ImageField(label="image")
