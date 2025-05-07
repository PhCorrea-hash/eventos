from django import forms
from .models import Grupo

# Forms para a criação de grupos
class GrupoForm(forms.ModelForm):
    class Meta:
        model = Grupo
        fields = ['nome', 'descricao']