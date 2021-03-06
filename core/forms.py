from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from .models import *
import datetime

class LaboratorioForm(forms.ModelForm):
    class Meta:
        model = Laboratorio
        fields = ['name']

    def clean_name(self):
        name = self.cleaned_data['name']

        if len(name) < 5:
            raise ValidationError(_('Limite mínimo de 5 caracteres'))

        return name

class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = ['name', 'color']

    def clean_name(self):
        name = self.cleaned_data['name']

        if len(name) < 5:
            raise ValidationError(_('Limite mínimo de 5 caracteres'))

        return name

class DisciplinaForm(forms.ModelForm):    
    class Meta:
        model = Disciplina
        fields = ['name']
    
    def clean_name(self):
        name = self.cleaned_data['name']

        if len(name) < 5:
            raise ValidationError(_('Limite mínimo de 5 caracteres'))

        return name

class ProfessorForm(forms.ModelForm):
    class Meta:
        model = Professor
        fields = '__all__'

    def clean_name(self):
        name = self.cleaned_data['name']

        if len(name) < 5:
            raise ValidationError(_('Limite mínimo de 5 caracteres'))

        return name

class ComputadorForm(forms.ModelForm):
    class Meta:
        model = Computador
        fields = ['codigo', 'patrimonio', 'dual_boot', 'funciona', 'processador', 'hd', 'ram', 'laboratorio', 'software']

        def clean_patrimonio(self):
            patrimonio = self.cleaned_data['patrimonio']

            if len(patrimonio) < 5:
                raise ValidationError(_('Patrimônio inválido'))

            return patrimonio

class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = '__all__'

        laboratorio = forms.ModelChoiceField(queryset=Laboratorio.objects.all(),required=False)
        professor = forms.ModelChoiceField(queryset=Professor.objects.all(),required=False)
        disciplina = forms.ModelChoiceField(queryset=Disciplina.objects.all(),required=False)
        curso = forms.ModelChoiceField(queryset=Curso.objects.all(),required=False)

    def clean(self):
        cleaned_data = super().clean()
        responsavel = cleaned_data.get("responsavel")
        evento = cleaned_data.get("evento")
        start_day = cleaned_data.get("start_day")
        end_day = cleaned_data.get("end_day")
        start_time = cleaned_data.get("start_time")
        end_time = cleaned_data.get("end_time")

        if len(evento) < 5 or len(responsavel) < 5:
            msg = 'Mínimo de 5 caracteres!'
            self.add_error('evento')
            self.add_error('responsavel')

        if start_day < datetime.date.today():
            msg = 'Esse dia já passou!'
            self.add_error('start_day', msg)

        if end_day < start_day:
            msg = 'Data inválida!'
            self.add_error('end_day', msg)

        if end_time < start_time:
            msg = 'Hora inválida!'
            self.add_error('end_time', msg)

class AulaForm(forms.ModelForm):
    class Meta:
        model = Aula
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        start_day = cleaned_data.get("start_day")
        end_day = cleaned_data.get("end_day")
        start_time = cleaned_data.get("start_time")
        end_time = cleaned_data.get("end_time")

        if end_day < start_day:
            msg = 'Data inválida!'
            self.add_error('end_day', msg)

        if end_time < start_time:
            msg = 'Hora inválida!'
            self.add_error('end_time', msg)

class EmprestimoForm(forms.ModelForm):
    class Meta:
        model = Emprestimo
        fields = ('date', 'evento', 'responsavel', 'email', 'contato', 'computador')

    def clean(self):
        cleaned_data = super().clean()
        responsavel = cleaned_data.get("responsavel")
        evento = cleaned_data.get("evento")
        date = cleaned_data.get("date")

        if len(evento) < 5 or len(responsavel) < 5:
            msg = 'Mínimo de 5 caracteres!'
            self.add_error('evento')
            self.add_error('responsavel')

        if date < datetime.date.today():
            msg = 'Esse dia já passou!'
            self.add_error('date', msg)

class SoftwareForm(forms.ModelForm):
    class Meta:
        model = Software
        fields = ('name', 'versao', 'tipo', 'descricao')

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get("name")
        
        if len(name) < 3:
            msg = 'Limite mínimo de 3 caracteres'
            self.add_error('name', msg)
            
class SolicitacaoReservaForm(forms.ModelForm):
    class Meta:
        model = SolicitacaoReserva
        fields = ['curso', 'disciplina', 'professor', 'software', 'dia', 'start_time', 'end_time', 'observacao', 'user']

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get("start_time")
        end_time = cleaned_data.get("end_time")

        if end_time < start_time:
            msg = 'Hora inválida!'
            self.add_error('end_time', msg)

class ManutencaoForm(forms.ModelForm):
    class Meta:
        model = Manutencao
        fields = ['pc_codigo', 'user']

# class RespostaSolicitacaoForm(forms.ModelForm):
#     class Meta:
#         model = RespostaSolicitacao
#         fields = ['resposta']