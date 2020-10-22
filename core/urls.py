from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    ## URLs Auth
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    ## URLs Laboratórios
    path('panel/laboratorio/cadastrar', CreateLaborationView.as_view(), name='laboratorio-create'),
    path('panel/laboratorio/<int:pk>', DetailLaboratorioView.as_view(), name='laboratorio-detail'),
    path('panel/laboratorio/updade/<int:pk>', UpdateLaboratorioView.as_view(), name='laboratorio-update'),
    path('panel/laboratorio/delete/<int:pk>', DeleteLaboratorioView.as_view(), name='laboratorio-delete'),
    ## URLs Cursos
    path('panel/curso/cadastrar', CreateCursoView.as_view(), name='curso-create'),
    path('panel/curso/<int:pk>', DetailCursoView.as_view(), name='curso-detail'),
    path('panel/curso/updade/<int:pk>', UpdateCursoView.as_view(), name='curso-update'),
    path('panel/curso/delete/<int:pk>', DeleteCursoView.as_view(), name='curso-delete'),
    ## URLs Disciplinas
    path('panel/disciplina/cadastrar', CreateDisciplinaView.as_view(), name='disciplina-create'),
    path('panel/disciplina/<int:pk>', DetailDisciplinaView.as_view(), name='disciplina-detail'),
    path('panel/disciplina/updade/<int:pk>', UpdateDisciplinaView.as_view(), name='disciplina-update'),
    path('panel/disciplina/delete/<int:pk>', DeleteDisciplinaView.as_view(), name='disciplina-delete'),
    ## URLs Professores
    path('panel/professor/cadastrar', CreateProfessorView.as_view(), name='professor-create'),
    path('panel/professor/<int:pk>', DetailProfessorView.as_view(), name='professor-detail'),
    path('panel/professor/updade/<int:pk>', UpdateProfessorView.as_view(), name='professor-update'),
    path('panel/professor/delete/<int:pk>', DeleteProfessorView.as_view(), name='professor-delete'),
    ## URLs Softwares
    path('panel/softwares/cadastrar', CreateSoftwareView.as_view(), name='software-create'),
    path('panel/softwares/<int:pk>', DetailSoftwareView.as_view(), name='software-detail'),
    path('panel/softwares/updade/<int:pk>', UpdateSoftwareView.as_view(), name='software-update'),
    path('panel/softwares/delete/<int:pk>', DeleteSoftwareView.as_view(), name='software-delete'),
    ## URLs Computadores
    path('panel/computador/cadastrar', CreateComputadorView.as_view(), name='computador-create'),
    path('panel/computador/<int:pk>', DetailComputadorView.as_view(), name='computador-detail'),
    path('panel/computador/updade/<int:pk>', UpdateComputadorView.as_view(), name='computador-update'),
    path('panel/computador/delete/<int:pk>', DeleteComputadorView.as_view(), name='computador-delete'),
    ## URLs Reservas
    path('panel/reserva/cadastrar', CreateReservaView.as_view(), name='reserva-create'),
    path('panel/reserva/<int:pk>', DetailReservaView.as_view(), name='reserva-detail'),
    path('panel/reserva/updade/<int:pk>', UpdateReservaView.as_view(), name='reserva-update'),
    path('panel/reserva/delete/<int:pk>', DeleteReservaView.as_view(), name='reserva-delete'),
    ## URLs Aulas
    path('panel/aula/cadastrar', CreateAulaView.as_view(), name='aula-create'),
    path('panel/aula/<int:pk>', DetailAulaView.as_view(), name='aula-detail'),
    path('panel/aula/updade/<int:pk>', UpdateAulaView.as_view(), name='aula-update'),
    path('panel/aula/delete/<int:pk>', DeleteAulaView.as_view(), name='aula-delete'),
    ## URL calendar
    path('panel/calendar', calendar, name='calendario'),
]