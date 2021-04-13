from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *

urlpatterns = [
    path('panel', IndexView.as_view(), name='index'),
    ## URLs Auth
    # path('', auth_views.LoginView.as_view(template_name='auth/login.html'), name='login'),
    # path('recuperar-senha/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset.html'), name='password_reset'),
	# path('recuperar-senha/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
	# path('recuperar-senha/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name="password_reset_confirm"),
	# path('recuperar-senha/complete/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
    # #path('registrar/', CreateUserView.as_view(), name='registrar'),
    # path('registrar/', cadastro, name='registrar'),
    # path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    ## URLs Usuários
    path('panel/usuarios/todos', ListUserView.as_view(), name='usuario-list'),
    path('panel/usuarios/<int:pk>', DetailUserView.as_view(), name='usuario-detail'),
    path('panel/usuarios/updade/<int:pk>', UpdateUserView.as_view(), name='usuario-update'),
    path('panel/usuarios/delete/<int:pk>', DeleteUserView.as_view(), name='usuario-delete'),
    ## URLs Laboratórios
    path('panel/laboratorio/cadastrar', CreateLaborationView.as_view(), name='laboratorio-create'),
    path('panel/laboratorio/<uuid:pk>', DetailLaboratorioView.as_view(), name='laboratorio-detail'),
    path('panel/laboratorio/updade/<uuid:pk>', UpdateLaboratorioView.as_view(), name='laboratorio-update'),
    path('panel/laboratorio/delete/<uuid:pk>', DeleteLaboratorioView.as_view(), name='laboratorio-delete'),
    ## URLs Cursos
    path('panel/curso/cadastrar', CreateCursoView.as_view(), name='curso-create'),
    path('panel/curso/<uuid:pk>', DetailCursoView.as_view(), name='curso-detail'),
    path('panel/curso/updade/<uuid:pk>', UpdateCursoView.as_view(), name='curso-update'),
    path('panel/curso/delete/<uuid:pk>', DeleteCursoView.as_view(), name='curso-delete'),
    ## URLs Disciplinas
    path('panel/disciplina/cadastrar', CreateDisciplinaView.as_view(), name='disciplina-create'),
    path('panel/disciplina/<uuid:pk>', DetailDisciplinaView.as_view(), name='disciplina-detail'),
    path('panel/disciplina/updade/<uuid:pk>', UpdateDisciplinaView.as_view(), name='disciplina-update'),
    path('panel/disciplina/delete/<uuid:pk>', DeleteDisciplinaView.as_view(), name='disciplina-delete'),
    ## URLs Professores
    path('panel/professor/cadastrar', CreateProfessorView.as_view(), name='professor-create'),
    path('panel/professor/<int:pk>', DetailProfessorView.as_view(), name='professor-detail'),
    path('panel/professor/updade/<int:pk>', UpdateProfessorView.as_view(), name='professor-update'),
    path('panel/professor/delete/<int:pk>', DeleteProfessorView.as_view(), name='professor-delete'),
    ## URLs Softwares
    path('panel/softwares/cadastrar', CreateSoftwareView.as_view(), name='software-create'),
    path('panel/softwares/<uuid:pk>', DetailSoftwareView.as_view(), name='software-detail'),
    path('panel/softwares/updade/<uuid:pk>', UpdateSoftwareView.as_view(), name='software-update'),
    path('panel/softwares/delete/<uuid:pk>', DeleteSoftwareView.as_view(), name='software-delete'),
    ## URLs Computadores
    path('panel/computador/cadastrar', CreateComputadorView.as_view(), name='computador-create'),
    path('panel/computador/<int:pk>', DetailComputadorView.as_view(), name='computador-detail'),
    path('panel/computador/updade/<int:pk>', UpdateComputadorView.as_view(), name='computador-update'),
    path('panel/computador/delete/<int:pk>', DeleteComputadorView.as_view(), name='computador-delete'),
    ## URLs Reservas
    path('panel/reserva/cadastrar', CreateReservaView.as_view(), name='reserva-create'),
    path('panel/reserva/<uuid:pk>', DetailReservaView.as_view(), name='reserva-detail'),
    path('panel/reserva/updade/<uuid:pk>', UpdateReservaView.as_view(), name='reserva-update'),
    path('panel/reserva/delete/<uuid:pk>', DeleteReservaView.as_view(), name='reserva-delete'),
    ## URLs Aulas
    path('panel/aula/cadastrar', CreateAulaView.as_view(), name='aula-create'),
    path('panel/aula/<uuid:pk>', DetailAulaView.as_view(), name='aula-detail'),
    path('panel/aula/updade/<uuid:pk>', UpdateAulaView.as_view(), name='aula-update'),
    path('panel/aula/delete/<uuid:pk>', DeleteAulaView.as_view(), name='aula-delete'),
    ## URLs Solicitacao Reservas
    path('panel/solicitacao/reserva/cadastrar', CreateSolicitacaoReservaView.as_view(), name='solicitacao-create'),
    path('panel/solicitacao/pendente', ListSolicitacaoReservaView.as_view(), name='solicitacao-list'),
    path('panel/solicitacao/minhas', ListMySolicitacaoReservaView.as_view(), name='solicitacao-mylist'),
    path('panel/solicitacao/todas', ListAllSolicitacaoReservaView.as_view(), name='solicitacao-alllist'),
    path('panel/solicitacao/detail/<uuid:pk>', DetailSolicitacaoReservaView.as_view(), name='solicitacao-detail'),
    path('panel/solicitacao/confirma', ConfirmaSolicitacao, name='solicitacao-confirmar'),
    path('panel/solicitacao/delete/<uuid:pk>', DeleteSolicitacaoReservaView.as_view(), name='solicitacao-delete'),
    #path('panel/resposta/solicitacao', RespostaSolicitacaoCreate, name='resposta-create'),
    ## URLs Emprestimo
    path('panel/emprestimo/cadastrar', CreateEmprestimoView.as_view(), name='emprestimo-create'),
    path('panel/emprestimo/<uuid:pk>', DetailEmprestimoView.as_view(), name='emprestimo-detail'),
    path('panel/emprestimo/updade/<uuid:pk>', UpdateEmprestimoView.as_view(), name='emprestimo-update'),
    path('panel/emprestimo/delete/<uuid:pk>', DeleteEmprestimoView.as_view(), name='emprestimo-delete'),
    ## URLs Manutenção
    path('panel/manutencao/cadastrar', CreateManutencaoView.as_view(), name='manutencao-create'),
    path('panel/manutencao/listar', ListManutencaoView.as_view(), name='manutencao-list'),
    path('panel/manutencao/detail/<uuid:pk>', DetailManutencaoView.as_view(), name='manutencao-detail'),
    path('panel/manutencao/update', UpdateManutencao, name='manutencao-update'),
    #path('panel/manutencao/update/<int:pk>', UpdateManutencaoView.as_view(), name='manutencao-update'),
    ## URL calendar
    path('panel/calendar', calendar, name='calendario'),
    ## URLs Relatórios
    path('panel/relatorios/<uuid:pk>', relatorios.as_view(), name='relatorio-index'),
]