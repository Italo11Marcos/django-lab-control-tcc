from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, ListView, DeleteView, DetailView, UpdateView, View, FormView
from .forms import *
from .models import *
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse, Http404, HttpResponseRedirect
from datetime import date
from accounts import models as accounts_models
from accounts import forms as accounts_forms


# Create your views here.
class IndexView(TemplateView):
    template_name = 'panel/index.html'

#View qnt de solicitações pendentes
def QntSolicitacoesPendentes(request):
    qntSolicitacoesPendentes = len(SolicitacaoReserva.objects.filter(status='P'))
    context = {
        'qnt': qntSolicitacoesPendentes
    }
    return render(request, 'layouts/base.html', context)

##Usuários CRUD##
class ListUserView(ListView):
    template_name = 'panel/usuario/list.html'
    model = accounts_models.CustomUsuario
    context_object_name = 'users'

class DetailUserView(DetailView):
    model = accounts_models.CustomUsuario
    template_name = 'panel/usuario/detail.html'
    context_object_name = 'user'

class UpdateUserView(UpdateView):
    model = accounts_models.CustomUsuario
    template_name = 'panel/usuario/update.html'
    form_class = accounts_forms.CustomUsuarioChangeForm
    context_object_name = 'user'
    #fields = ['first_name', 'last_name', 'masp', 'username', 'is_staff']
    success_url = reverse_lazy('usuario-list')

    def form_valid(self, form, *args, **kwargs):
        messages.success(self.request, 'Usuário editado com sucesso!')
        return super().form_valid(form)

    def form_invalid(self, form, *args, **kwargs):
        messages.error(self.request, 'Tivemos algum problema')
        return super().form_valid(form)

class DeleteUserView(DeleteView):
    model = accounts_models.CustomUsuario
    success_url = reverse_lazy('usuario-list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        messages.success(self.request, 'Usuário excluído com sucesso!')
        success_url = self.get_success_url()
        return HttpResponseRedirect(success_url)

##Laboratorios CRUD##
class CreateLaborationView(CreateView):
    model = Laboratorio
    form_class = LaboratorioForm
    template_name = 'panel/laboratorio/create.html'
    success_url = reverse_lazy('laboratorio-create')

    def get_context_data(self, **kwargs):
        context = super(CreateLaborationView, self).get_context_data(**kwargs)
        context['laboratorios'] = Laboratorio.objects.order_by('?').all()
        return context

    def form_valid(self, form, *args, **kwargs):
        messages.success(self.request, 'Laboratório cadastrado com sucesso!')
        return super(CreateLaborationView, self).form_valid(form)

    def form_invalid(self, form, *args, **kwargs):
        messages.error(self.request, 'Tivemos algum problema')
        return super(CreateLaborationView, self).form_invalid(form)

class DetailLaboratorioView(DetailView):
    model = Laboratorio
    template_name = 'panel/laboratorio/detail.html'
    
    def get_context_data(self, **kwargs):
        context = super(DetailLaboratorioView, self).get_context_data(**kwargs)
        pcs = Computador.objects.filter(laboratorio=self.get_object().pk)
        context['pcs'] = pcs
        context['qnt'] = len(pcs)
        return context

class UpdateLaboratorioView(UpdateView):
    model = Laboratorio
    template_name = 'panel/laboratorio/update.html'
    fields = ['name', 'qnt_computador']
    success_url = reverse_lazy('laboratorio-create')

    def form_valid(self, form, *args, **kwargs):
        messages.success(self.request, 'Laboratório editado com sucesso!')
        return super().form_valid(form)

    def form_invalid(self, form, *args, **kwargs):
        messages.error(self.request, 'Tivemos algum problema')
        return super().form_valid(form)

class DeleteLaboratorioView(DeleteView):
    model = Laboratorio
    success_url = reverse_lazy('laboratorio-create')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        messages.success(self.request, 'Laboratório excluído com sucesso!')
        success_url = self.get_success_url()
        return HttpResponseRedirect(success_url)
    
##Cursos CRUD##
class CreateCursoView(UserPassesTestMixin ,CreateView):
    login_url = 'login'
    form_class = CursoForm
    template_name = 'panel/curso/create.html'
    success_url = reverse_lazy('curso-create')

    def test_func(self):
        if self.request.user.is_staff:
            return True
        else:
            raise Http404('Você não tem permissão')

    def get_context_data(self, **kwargs):
        context = super(CreateCursoView, self).get_context_data(**kwargs)
        context['cursos'] = Curso.objects.order_by('?').all()
        return context

    def form_valid(self, form, *args, **kwargs):
        messages.success(self.request, 'Curso cadastrado com sucesso!')
        return super(CreateCursoView, self).form_valid(form)

    def form_invalid(self, form, *args, **kwargs):
        messages.error(self.request, 'Tivemos algum problema')
        return super(CreateCursoView, self).form_invalid(form)

class DetailCursoView(DetailView):
    model = Curso
    template_name = 'panel/curso/detail.html'
    context_object_name = 'curso'

    def get_context_data(self, **kwargs):
        context = super(DetailCursoView, self).get_context_data(**kwargs)
        aulas = Aula.objects.filter(curso=self.get_object().pk)
        reservas = Reserva.objects.filter(curso=self.get_object().pk)
        context['qnt'] = len(aulas) + len(reservas)
        return context

class UpdateCursoView(UpdateView):
    model = Curso
    template_name = 'panel/curso/update.html'
    fields = ['name']
    success_url = reverse_lazy('curso-create')

    def form_valid(self, form, *args, **kwargs):
        messages.success(self.request, 'Curso editado com sucesso!')
        return super().form_valid(form)

    def form_invalid(self, form, *args, **kwargs):
        messages.error(self.request, 'Tivemos algum problema')
        return super().form_valid(form)

class DeleteCursoView(DeleteView):
    model = Curso
    success_url = reverse_lazy('curso-create')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        messages.success(self.request, 'Curso excluído com sucesso!')
        success_url = self.get_success_url()
        return HttpResponseRedirect(success_url)

##Disciplina CRUD##
class CreateDisciplinaView(CreateView):
    model = Disciplina
    form_class = DisciplinaForm
    template_name = 'panel/disciplina/create.html'
    success_url = reverse_lazy('disciplina-create')

    def get_context_data(self, **kwargs):
        context = super(CreateDisciplinaView, self).get_context_data(**kwargs)
        context['disciplinas'] = Disciplina.objects.order_by('?').all()
        return context

    def form_valid(self, form, *args, **kwargs):
        messages.success(self.request, 'Disciplina cadastrada com sucesso!')
        return super(CreateDisciplinaView, self).form_valid(form)

    def form_invalid(self, form, *args, **kwargs):
        messages.error(self.request, 'Tivemos algum problema')
        return super(CreateDisciplinaView, self).form_invalid(form)

class DetailDisciplinaView(DetailView):
    model = Disciplina
    template_name = 'panel/disciplina/detail.html'
    context_object_name = 'disciplina'

    def get_context_data(self, **kwargs):
        context = super(DetailDisciplinaView, self).get_context_data(**kwargs)
        aulas = Aula.objects.filter(disciplina=self.get_object().pk)
        reservas = Reserva.objects.filter(disciplina=self.get_object().pk)
        context['qnt'] = len(aulas) + len(reservas)
        return context

class UpdateDisciplinaView(UpdateView):
    model = Disciplina
    template_name = 'panel/disciplina/update.html'
    fields = ['name']
    success_url = reverse_lazy('disciplina-create')

    def form_valid(self, form, *args, **kwargs):
        messages.success(self.request, 'Disciplina editada com sucesso!')
        return super().form_valid(form)

    def form_invalid(self, form, *args, **kwargs):
        messages.error(self.request, 'Tivemos algum problema')
        return super().form_valid(form)

class DeleteDisciplinaView(DeleteView):
    model = Disciplina
    success_url = reverse_lazy('disciplina-create')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        messages.success(self.request, 'disciplina excluída com sucesso!')
        success_url = self.get_success_url()
        return HttpResponseRedirect(success_url)

##Professor CRUD##
class CreateProfessorView(CreateView):
    form_class = ProfessorForm
    template_name = 'panel/professor/create.html'
    success_url = reverse_lazy('professor-create')

    def get_context_data(self, **kwargs):
        context = super(CreateProfessorView, self).get_context_data(**kwargs)
        context['professors'] = Professor.objects.order_by('?').all()
        return context

    def form_valid(self, form, *args, **kwargs):
        messages.success(self.request, 'Professor(a) cadastrado(a) com sucesso!')
        return super(CreateProfessorView, self).form_valid(form)

    def form_invalid(self, form, *args, **kwargs):
        messages.error(self.request, 'Tivemos algum problema')
        return super(CreateProfessorView, self).form_invalid(form)

class DetailProfessorView(DetailView):
    model = Professor
    template_name = 'panel/professor/detail.html'
    context_object_name = 'professor'

class UpdateProfessorView(UpdateView):
    model = Professor
    template_name = 'panel/professor/update.html'
    fields = '__all__'
    success_url = reverse_lazy('professor-create')

    def form_valid(self, form, *args, **kwargs):
        messages.success(self.request, 'Professor(a) editado(a) com sucesso!')
        return super().form_valid(form)

    def form_invalid(self, form, *args, **kwargs):
        messages.error(self.request, 'Tivemos algum problema')
        return super().form_valid(form)

class DeleteProfessorView(DeleteView):
    model = Professor
    success_url = reverse_lazy('professor-create')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        messages.success(self.request, 'Professor(a) excluído(o) com sucesso!')
        success_url = self.get_success_url()
        return HttpResponseRedirect(success_url)

##Software CRUD##
class CreateSoftwareView(CreateView):
    form_class = SoftwareForm
    template_name = 'panel/software/create.html'
    success_url = reverse_lazy('software-create')

    def get_context_data(self, **kwargs):
        context = super(CreateSoftwareView, self).get_context_data(**kwargs)
        context['softwares'] = Software.objects.order_by('?').all()
        return context

    def form_valid(self, form, *args, **kwargs):
        messages.success(self.request, 'Software cadastrado com sucesso!')
        return super(CreateSoftwareView, self).form_valid(form)

    def form_invalid(self, form, *args, **kwargs):
        messages.error(self.request, 'Tivemos algum problema')
        return super(CreateSoftwareView, self).form_invalid(form)

class DetailSoftwareView(DetailView):
    model = Software
    template_name = 'panel/software/detail.html'
    context_object_name = 'software'

    def get_context_data(self, **kwargs):
        context = super(DetailSoftwareView, self).get_context_data(**kwargs)
        pcs = Computador.objects.filter(software=self.get_object().pk)
        context['pcs'] = pcs
        context['qnt'] = len(pcs)
        return context

class UpdateSoftwareView(UpdateView):
    model = Software
    template_name = 'panel/software/update.html'
    fields = ['name', 'versao', 'tipo', 'descricao']
    success_url = reverse_lazy('software-create')

    def form_valid(self, form, *args, **kwargs):
        messages.success(self.request, 'Software editado com sucesso!')
        return super().form_valid(form)

    def form_invalid(self, form, *args, **kwargs):
        messages.error(self.request, 'Tivemos algum problema')
        return super().form_invalid(form)

class DeleteSoftwareView(DeleteView):
    model = Software
    success_url = reverse_lazy('software-create')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        messages.success(self.request, 'Software excluído com sucesso!')
        success_url = self.get_success_url()
        return HttpResponseRedirect(success_url)

##Computador CRUD##
class CreateComputadorView(CreateView):
    form_class = ComputadorForm
    template_name = 'panel/computador/create.html'
    success_url = reverse_lazy('computador-create')

    def get_context_data(self, **kwargs):
        context = super(CreateComputadorView, self).get_context_data(**kwargs)
        context['computadors'] = Computador.objects.order_by('?').all()
        context['softwares'] = Software.objects.all()
        return context

    def form_valid(self, form, *args, **kwargs):
        messages.success(self.request, 'Computador cadastrado com sucesso!')
        return super(CreateComputadorView, self).form_valid(form)

    def form_invalid(self, form, *args, **kwargs):
        messages.error(self.request, 'Tivemos algum problema')
        return super(CreateComputadorView, self).form_invalid(form)

class DetailComputadorView(DetailView):
    model = Computador
    template_name = 'panel/computador/detail.html'
    context_object_name = 'computador'

class UpdateComputadorView(UpdateView):
    model = Computador
    template_name = 'panel/computador/update.html'
    fields = ['codigo', 'patrimonio', 'dual_boot', 'funciona', 'processador', 'hd', 'ram', 'laboratorio', 'software']
    success_url = reverse_lazy('computador-create')

    def form_valid(self, form, *args, **kwargs):
        messages.success(self.request, 'Computador editado com sucesso!')
        return super().form_valid(form)

    def form_invalid(self, form, *args, **kwargs):
        messages.error(self.request, 'Tivemos algum problema')
        return super().form_valid(form)

class DeleteComputadorView(DeleteView):
    model = Computador
    success_url = reverse_lazy('computador-create')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        messages.success(self.request, 'Computador excluído com sucesso!')
        success_url = self.get_success_url()
        return HttpResponseRedirect(success_url)

##Reserva CRUD##
class CreateReservaView(CreateView):
    form_class = ReservaForm
    template_name = 'panel/reserva/create.html'
    success_url = reverse_lazy('reserva-create')

    def get_context_data(self, **kwargs):
        context = super(CreateReservaView, self).get_context_data(**kwargs)
        context['reservas'] = Reserva.objects.order_by('?').all()
        return context

    def form_valid(self, form, *args, **kwargs):
        messages.success(self.request, 'Reserva cadastrada com sucesso!')
        return super(CreateReservaView, self).form_valid(form)

    def form_invalid(self, form, *args, **kwargs):
        messages.error(self.request, 'Tivemos algum problema')
        return super(CreateReservaView, self).form_invalid(form)

class DetailReservaView(DetailView):
    model = Reserva
    template_name = 'panel/reserva/detail.html'
    context_object_name = 'reserva'

class UpdateReservaView(UpdateView):
    model = Reserva
    template_name = 'panel/reserva/update.html'
    fields = '__all__'
    success_url = reverse_lazy('reserva-create')

    def form_valid(self, form, *args, **kwargs):
        messages.success(self.request, 'Reserva editada com sucesso!')
        return super().form_valid(form)

    def form_invalid(self, form, *args, **kwargs):
        messages.error(self.request, 'Tivemos algum problema')
        return super().form_valid(form)

class DeleteReservaView(DeleteView):
    model = Reserva
    success_url = reverse_lazy('reserva-create')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        messages.success(self.request, 'Reserva excluído com sucesso!')
        success_url = self.get_success_url()
        return HttpResponseRedirect(success_url)

##Aula CRUD##
class CreateAulaView(CreateView):
    form_class = AulaForm
    template_name = 'panel/aula/create.html'
    success_url = reverse_lazy('aula-create')

    def get_context_data(self, **kwargs):
        context = super(CreateAulaView, self).get_context_data(**kwargs)
        context['aulas'] = Aula.objects.order_by('?').all()
        return context

    def form_valid(self, form, *args, **kwargs):
        messages.success(self.request, 'Aula cadastrada com sucesso!')
        return super(CreateAulaView, self).form_valid(form)

    def form_invalid(self, form, *args, **kwargs):
        messages.error(self.request, 'Tivemos algum problema')
        return super(CreateAulaView, self).form_invalid(form)

class DetailAulaView(DetailView):
    model = Aula
    template_name = 'panel/aula/detail.html'
    context_object_name = 'aula'

class UpdateAulaView(UpdateView):
    model = Aula
    template_name = 'panel/aula/update.html'
    fields = '__all__'
    success_url = reverse_lazy('aula-create')

    def form_valid(self, form, *args, **kwargs):
        messages.success(self.request, 'Aula editada com sucesso!')
        return super().form_valid(form)

    def form_invalid(self, form, *args, **kwargs):
        messages.error(self.request, 'Tivemos algum problema')
        return super().form_valid(form)

class DeleteAulaView(DeleteView):
    model = Aula
    success_url = reverse_lazy('aula-create')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        messages.success(self.request, 'Aula excluída com sucesso!')
        success_url = self.get_success_url()
        return HttpResponseRedirect(success_url)

##Solicitação Reserva CRUD##
class CreateSolicitacaoReservaView(CreateView):
    form_class = SolicitacaoReservaForm
    template_name = 'panel/solicitacao/create.html'
    success_url = reverse_lazy('solicitacao-create')

    def get_context_data(self, **kwargs):
        context = super(CreateSolicitacaoReservaView, self).get_context_data(**kwargs)
        context['softwares'] = Software.objects.all()
        return context

    def form_valid(self, form, *args, **kwargs):
        form = SolicitacaoReservaForm(self.request.POST)
        solicitacao = form.save(commit=False)
        solicitacao.user = self.request.user
        solicitacao.save()
        messages.success(self.request, 'Solicitação Realizada com sucesso')
        return super(CreateSolicitacaoReservaView, self).form_valid(form)

    def form_invalid(self, form, *args, **kwargs):
        messages.error(self.request, 'Tivemos algum problema')
        return super(CreateSolicitacaoReservaView, self).form_invalid(form)

class ListSolicitacaoReservaView(ListView):
    model = SolicitacaoReserva
    template_name = 'panel/solicitacao/list.html'

    def get_context_data(self, **kwargs):
        context = super(ListSolicitacaoReservaView, self).get_context_data(**kwargs)
        context['solicitacao'] = SolicitacaoReserva.objects.filter(status='P')
        return context

class ListMySolicitacaoReservaView(ListView):
    model = SolicitacaoReserva
    template_name = 'panel/solicitacao/mylist.html'

    def get_context_data(self, **kwargs):
        context = super(ListMySolicitacaoReservaView, self).get_context_data(**kwargs)
        context['solicitacao'] = SolicitacaoReserva.objects.filter(user=self.request.user.id)
        return context

class ListAllSolicitacaoReservaView(ListView):
    model = SolicitacaoReserva
    template_name = 'panel/solicitacao/alllist.html'
    context_object_name = 'solicitacao'

class DetailSolicitacaoReservaView(DetailView):
    model = SolicitacaoReserva
    template_name = 'panel/solicitacao/detail.html'
    context_object_name = 'solicitacao'

    def get_context_data(self, **kwargs):
        context = super(DetailSolicitacaoReservaView, self).get_context_data(**kwargs)
        resp = RespostaSolicitacao.objects.filter(solicitacao=self.get_object().pk)
        resposta = '0'
        if resp:
            resposta = resp[0].resposta
        context['resp'] = resposta
        return context

class UpdateSolicitacaoReservaView(UpdateView):
    model = SolicitacaoReserva
    template_name = 'panel/solicitacao/update.html'
    form_class = SolicitacaoReservaForm
    success_url = reverse_lazy('solicitacao-list')

    def form_valid(self, form, *args, **kwargs):
        messages.success(self.request, 'Solicitacao editada com sucesso!')
        return super().form_valid(form)

    def form_invalid(self, form, *args, **kwargs):
        messages.error(self.request, 'Tivemos algum problema')
        return super().form_valid(form)

class DeleteSolicitacaoReservaView(DeleteView):
    model = SolicitacaoReserva
    success_url = reverse_lazy('solicitacao-list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        messages.success(self.request, 'Solicitacao excluída com sucesso!')
        success_url = self.get_success_url()
        return HttpResponseRedirect(success_url)

def RespostaSolicitacaoCreate(request):
    if request.method == 'POST':
        solicitacaoreserva = request.POST.get('solicitacaoreserva_id', False)
        user = request.POST.get('user_id', False)
        resposta = request.POST.get('resposta', False)
        s = SolicitacaoReserva.objects.get(pk=solicitacaoreserva)
        u = accounts_models.CustomUsuario.objects.get(pk=user)
        s.status = 'F'
        s.save()
        r = RespostaSolicitacao.objects.create(user=u, solicitacao=s, resposta=resposta)
        r.save()
        messages.success(request, 'Respondido com sucesso!')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
##Emprestimo CRUD##
class CreateEmprestimoView(CreateView):
    form_class = EmprestimoForm
    template_name = 'panel/emprestimo/create.html'
    success_url = reverse_lazy('emprestimo-create')

    def get_context_data(self, **kwargs):
        context = super(CreateEmprestimoView, self).get_context_data(**kwargs)
        context['emprestimos'] = Emprestimo.objects.order_by('?').all()
        return context

    def form_valid(self, form, *args, **kwargs):
        form = EmprestimoForm(self.request.POST)
        emprestimo = form.save(commit=False)
        emprestimo.user_id = self.request.user
        emprestimo.save()
        messages.success(self.request, 'Solicitação Realizada com sucesso')
        return super(CreateEmprestimoView, self).form_valid(form)

    def form_invalid(self, form, *args, **kwargs):
        messages.error(self.request, 'Tivemos algum problema')
        return super(CreateEmprestimoView, self).form_invalid(form)

class DetailEmprestimoView(DetailView):
    model = Emprestimo
    template_name = 'panel/emprestimo/detail.html'
    context_object_name = 'emprestimo'

class UpdateEmprestimoView(UpdateView):
    model = Emprestimo
    template_name = 'panel/emprestimo/update.html'
    form_class = EmprestimoForm
    success_url = reverse_lazy('emprestimo-create')

    def form_valid(self, form, *args, **kwargs):
        messages.success(self.request, 'Empréstimo editado com sucesso!')
        return super().form_valid(form)

    def form_invalid(self, form, *args, **kwargs):
        messages.error(self.request, 'Tivemos algum problema')
        return super().form_valid(form)

class DeleteEmprestimoView(DeleteView):
    model = Emprestimo
    success_url = reverse_lazy('emprestimo-create')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        messages.success(self.request, 'Empréstimo excluído com sucesso!')
        success_url = self.get_success_url()
        return HttpResponseRedirect(success_url)

##Manutenção CRUD##
class CreateManutencaoView(CreateView):
    form_class = ManutencaoForm
    success_url = reverse_lazy('manutencao-list')

    def form_valid(self, form, *args, **kwargs):
        form = ManutencaoForm(self.request.POST)
        #print(self.request.POST.get('pc_codigo'))
        manutencao = form.save(commit=False)
        pc = Computador.objects.get(pk=self.request.POST.get('pc_codigo'))
        pc.qnt_manutencao += 1
        pc.em_manutencao = True
        pc.save()
        manutencao.user_masp = self.request.user
        manutencao.save()
        messages.success(self.request, 'Manutenção iniciado com sucesso')
        return super(CreateManutencaoView, self).form_valid(form)

    def form_invalid(self, form, *args, **kwargs):
        messages.error(self.request, 'Tivemos algum problema')
        return super(CreateManutencaoView, self).form_invalid(form)

class ListManutencaoView(ListView):
    model = Manutencao
    template_name = 'panel/manutencao/list.html'

    def get_context_data(self, **kwargs):
        context = super(ListManutencaoView, self).get_context_data(**kwargs)
        context['manutencoes'] = Manutencao.objects.all()
        return context

class DetailManutencaoView(DetailView):
    model = Manutencao
    template_name = 'panel/manutencao/detail.html'
    context_object_name = 'manutencao'

def UpdateManutencao(request):
    if request.method == 'POST':
        manutecao = request.POST.get('manutencao_id', False)
        descricao = request.POST.get('descricao', False)
        m = Manutencao.objects.get(pk=manutecao)
        m.descricao = descricao
        m.status = 'Resolvido'
        m.data_fim = date.today()
        m.save()
        messages.success(request, 'Respondido com sucesso!')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

##calendar
def calendar(request):
    reservas = Reserva.objects.all()
    aulas = Aula.objects.all()
    context = {
        "reservas": reservas,
        "aulas": aulas
    }
    return render(request, 'panel/reserva/calendario.html', context)





