from django import forms
from .models import Paciente

class PacienteForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    es_profesional = forms.BooleanField(
        required=False, 
        label="¿Eres un profesional?", 
        widget=forms.CheckboxInput()
    )

    class Meta:
        model = Paciente
        fields = ['nombre', 'apellido', 'email', 'password', 'es_profesional']

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

class DatosPacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ['edad', 'peso', 'altura', 'sexo']
        
class PacienteFotoForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ['foto_perfil']
        
        
