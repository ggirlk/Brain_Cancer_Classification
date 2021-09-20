from django import forms
from .models import *


class brain_MRI_form(forms.ModelForm):

    class Meta:
        model = brain_MRI
        fields = ['MRI_image']
