from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, ListView, DeleteView, DetailView, UpdateView
from .forms import *
from .models import *
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse, Http404

# Create your views here.
class IndexView(TemplateView):
    template_name = 'panel/index.html'


def cadastro(request): 
    if request.method == "POST":
        form = CustomUsuarioCreateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cadastro Realizado com Sucesso')
            return redirect('login')
        else:
            messages.error(request, 'Tivemos algum problema')
    else:
        form = CustomUsuarioCreateForm()
    context = {
        'form': form
    }
    return render(request, 'auth/register.html', context)

class ListUserView(ListView):
    template_name = 'panel/usuario/list.html'
    model = CustomUsuario
    context_object_name = 'users'

class DetailUserView(DetailView):
    model = CustomUsuario
    template_name = 'panel/usuario/detail.html'
    context_object_name = 'user'

class UpdateUserView(UpdateView):
    model = CustomUsuario
    template_name = 'panel/usuario/update.html'
    form_class = CustomUsuarioChangeForm
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
    model = CustomUsuario
    success_url = reverse_lazy('usuario-list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        messages.success(self.request, 'Usuário excluído com sucesso!')
        success_url = self.get_success_url()
        return HttpResponseRedirect(success_url)

##Laboratorios CRUD##
class CreateLaborationView(CreateView):
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
        return super(CreateLaborationView, self).form_valid(form)

class DetailLaboratorioView(DetailView):
    model = Laboratorio
    template_name = 'panel/laboratorio/detail.html'
    context_object_name = 'laboratorio'

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
        return super(CreateCursoView, self).form_valid(form)

class DetailCursoView(DetailView):
    model = Curso
    template_name = 'panel/curso/detail.html'
    context_object_name = 'curso'

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
        return super(CreateDisciplinaView, self).form_valid(form)

class DetailDisciplinaView(DetailView):
    model = Disciplina
    template_name = 'panel/disciplina/detail.html'
    context_object_name = 'disciplina'

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
        return super(CreateProfessorView, self).form_valid(form)

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
        return super(CreateSoftwareView, self).form_valid(form)

class DetailSoftwareView(DetailView):
    model = Software
    template_name = 'panel/software/detail.html'
    context_object_name = 'software'

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
        return context

    def form_valid(self, form, *args, **kwargs):
        messages.success(self.request, 'Computador cadastrado com sucesso!')
        return super(CreateComputadorView, self).form_valid(form)

    def form_invalid(self, form, *args, **kwargs):
        messages.error(self.request, 'Tivemos algum problema')
        return super(CreateComputadorView, self).form_valid(form)

class DetailComputadorView(DetailView):
    model = Computador
    template_name = 'panel/computador/detail.html'
    context_object_name = 'computador'

class UpdateComputadorView(UpdateView):
    model = Computador
    template_name = 'panel/computador/update.html'
    fields = '__all__'
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
        return super(CreateReservaView, self).form_valid(form)

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
        return super(CreateAulaView, self).form_valid(form)

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

    def form_valid(self, form, *args, **kwargs):
        form = SolicitacaoReservaForm(self.request.POST)
        solicitacao = form.save(commit=False)
        solicitacao.user_masp = self.request.user
        solicitacao.save()
        messages.success(self.request, 'Solicitação Realizada com sucesso')
        return super(CreateSolicitacaoReservaView, self).form_valid(form)

    def form_invalid(self, form, *args, **kwargs):
        messages.error(self.request, 'Tivemos algum problema')
        return super(CreateSolicitacaoReservaView, self).form_valid(form)

class ListSolicitacaoReservaView(ListView):
    model = SolicitacaoReserva
    template_name = 'panel/solicitacao/list.html'

    def get_context_data(self, **kwargs):
        context = super(ListSolicitacaoReservaView, self).get_context_data(**kwargs)
        context['solicitacao'] = SolicitacaoReserva.objects.filter(status='P')
        return context

class DetailSolicitacaoReservaView(DetailView):
    model = SolicitacaoReserva
    template_name = 'panel/solicitacao/detail.html'
    context_object_name = 'solicitacao'

class UpdateSolicitacaoReservaView(UpdateView):
    model = Aula
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
##calendar
def calendar(request):
    reservas = Reserva.objects.all()
    context = {
        "reservas": reservas
    }
    return render(request, 'panel/reserva/calendario.html', context)






