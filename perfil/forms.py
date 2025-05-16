from django import forms
from django.contrib.auth.models import User
from .models import Perfil

class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['telefone', 'data_nascimento', 'endereco']
        widgets = {
            'data_nascimento': forms.DateInput(attrs={'placeholder': 'xx/xx/xxxx'}),
            'telefone': forms.DateInput(attrs={'placeholder': '(12)34567-8910'}),
            'endereco': forms.DateInput(attrs={'placeholder': 'Av./Rua'}),
        }

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name']
        widgets = {
            'username': forms.DateInput(attrs={'placeholder': 'Usuário'}),
            'email': forms.DateInput(attrs={'placeholder': 'E-mail'}),
            'first_name': forms.DateInput(attrs={'placeholder': 'Nome'}),
        }

class FotoPerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['foto_perfil']