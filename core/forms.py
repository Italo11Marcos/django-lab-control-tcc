from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import *

class CustomUsuarioCreateForm(UserCreationForm):

    class Meta:
        model = CustomUsuario
        fields = ('first_name', 'last_name', 'masp','username')
        labels = {'username': 'Username/E-mail'}

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.email = self.cleaned_data["username"]
        if commit:
            user.save()
        return user

class CustomUsuarioChangeForm(UserChangeForm):

    class Meta:
        model = CustomUsuario
        fields = ('first_name', 'last_name', 'masp', 'username', 'is_staff')

class LaboratorioForm(forms.ModelForm):
    class Meta:
        model = Laboratorio
        fields = ('name', 'qnt_computador')
    
class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = ['name']

class DisciplinaForm(forms.ModelForm):
    class Meta:
        model = Disciplina
        fields = ['name']

class ProfessorForm(forms.ModelForm):
    class Meta:
        model = Professor
        fields = '__all__'

class ComputadorForm(forms.ModelForm):
    class Meta:
        model = Computador
        fields = '__all__'

class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = '__all__'

        laboratorio_id = forms.ModelChoiceField(queryset=Laboratorio.objects.all(),required=False)
        professor_id = forms.ModelChoiceField(queryset=Professor.objects.all(),required=False)
        disciplina_id = forms.ModelChoiceField(queryset=Disciplina.objects.all(),required=False)
        curso_id = forms.ModelChoiceField(queryset=Curso.objects.all(),required=False)

class AulaForm(forms.ModelForm):
    class Meta:
        model = Aula
        fields = '__all__'

class EmprestimoForm(forms.ModelForm):
    class Meta:
        model = Emprestimo
        fields = ('date', 'evento', 'responsavel', 'email', 'contato', 'computador_codigo')

class SoftwareForm(forms.ModelForm):
    class Meta:
        model = Software
        fields = ('name', 'versao', 'tipo', 'descricao')

class SolicitacaoReservaForm(forms.ModelForm):
    class Meta:
        model = SolicitacaoReserva
        fields = ('qnt_alunos', 'professor_masp', 'curso_id', 'disciplina_id', 'software_id', 'observacao')

class RespostaSolicitacaoForm(forms.ModelForm):
    class Meta:
        model = RespostaSolicitacao
        fields = ['resposta']

class ManutencaoForm(forms.ModelForm):
    class Meta:
        model = Manutencao
        fields = ['pc_codigo', 'user_masp']

