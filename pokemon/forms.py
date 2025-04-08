from django import forms
from .models import Equipo, Pokemon

class EquipoForm(forms.ModelForm):
    class Meta:
        model = Equipo
        fields = ['nombre', 'pokemones']
        widgets = {
            'pokemones': forms.CheckboxSelectMultiple,
        }
