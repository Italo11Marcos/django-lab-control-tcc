from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import *

class CustomUsuarioCreationForm(UserCreationForm):
    class Meta:
        model = CustomUsuario
        fields = ('first_name', 'last_name', 'masp')
        labels = {'username': 'E-mail'}

        def save(self, commit=True):
            user = super().save(commit=False)
            user.set_password(self.cleaned_data['password1'])
            user.email = self.cleaned_data['username']
            if commit:
                user.save()
            return user

class CustomUsuarioChangeForm(UserChangeForm):
    class Meta:
        model = CustomUsuario
        fields = ('first_name', 'last_name', 'masp')
        labels = {'username': 'E-mail'}

class LaboratorioForm(forms.ModelForm):
    class Meta:
        model = Laboratorio
        fields = '__all__'
    
class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = '__all__'

class DisciplinaForm(forms.ModelForm):
    class Meta:
        model = Disciplina
        fields = '__all__'

class ProfessorForm(forms.ModelForm):
    class Meta:
        model = Professor
        fields = '__all__'

class ComputatorForm(forms.ModelForm):
    class Meta:
        model = Computador
        fields = '__all__'

class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = '__all__'

class EmprestimoForm(forms.ModelForm):
    class Meta:
        model = Emprestimo
        fields = '__all__'

class SoftwareForm(forms.ModelForm):
    class Meta:
        model = Software
        fields = '__all__'


