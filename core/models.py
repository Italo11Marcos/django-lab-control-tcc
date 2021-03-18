from django.db import models
from accounts import models as accounts_models
import uuid

class Curso(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=45, unique=True)

    def __str__(self):
        return self.name

class Disciplina(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=70, unique=True)

    def __str__(self):
        return self.name

class Professor(models.Model):
    masp = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    contato = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return self.name

class Laboratorio(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=45, unique=True)
    qnt_computador = models.IntegerField(blank=True, default=0)

    def __str__(self):
        return self.name

class Software(models.Model):

    TIPO_CHOICES = [
        ('SL', 'Software Livre'),
        ('SP', 'Software Licenciado'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    versao = models.CharField(max_length=15)
    tipo = models.CharField(choices=TIPO_CHOICES, max_length=2, default='SL')
    descricao = models.TextField()

    def __str__(self):
        return self.name

class Computador(models.Model):

    RAM_CHOICES = [
        ('1GB', '1GB'),
        ('2GB', '2GB'),
        ('3GB', '3GB'),
        ('4GB', '4GB'),
    ]

    HD_CHOICES = [
        ('100GB', '100GB'),
        ('200GB', '200GB'),
        ('300GB', '300GB'),
        ('400GB', '400GB'),
        ('500GB', '500GB'),
    ]

    PROCESSADOR_CHOICES = [
        ('I2', 'Intel Core 2 Duo'),
        ('I3', 'Intel I3'),
        ('I5', 'Intel I5'),
        ('IP', 'Intel Pentium Dual Core'),
    ]

    codigo = models.IntegerField(primary_key=True)
    patrimonio = models.CharField(max_length=15, unique=True)
    dual_boot = models.BooleanField(default=False)
    funciona = models.BooleanField(default=True)
    processador = models.CharField(choices=PROCESSADOR_CHOICES, max_length=2, default='I2')
    hd = models.CharField(choices=HD_CHOICES, max_length=5, default='100GB')
    ram = models.CharField(choices=RAM_CHOICES, max_length=3, default='1GB')
    laboratorio = models.ForeignKey(Laboratorio, on_delete=models.SET_NULL, null=True)
    software = models.ManyToManyField(Software)
    qnt_manutencao = models.IntegerField(default=0)
    em_manutencao = models.BooleanField(default=False)

    def __str__(self):
        return str(self.codigo)

class Reserva(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    evento = models.CharField(max_length=100)
    responsavel = models.CharField(max_length=100)
    contato = models.CharField(max_length=15)
    email = models.EmailField()
    start_day = models.DateField()
    end_day = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    laboratorio = models.ForeignKey(Laboratorio, on_delete=models.SET_NULL, null=True, blank=True)
    curso = models.ForeignKey(Curso, on_delete=models.SET_NULL, null=True, blank=True)
    disciplina = models.ForeignKey(Disciplina, on_delete=models.SET_NULL, null=True, blank=True)
    professor = models.ForeignKey(Professor, on_delete=models.SET_NULL, null=True, blank=True)

class Aula(models.Model):

    DIA_CHOICES = [
        ('1', 'Segunda'),
        ('2', 'Terça'),
        ('3', 'Quarta'),
        ('4', 'Quinta'),
        ('5', 'Sexta'),
        ('6', 'Sabado'),
        ('7', 'Domingo'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    dia = models.CharField(choices=DIA_CHOICES, max_length=1)
    start_time = models.TimeField()
    end_time = models.TimeField()
    start_day = models.DateField()
    end_day = models.DateField()
    laboratorio = models.ForeignKey(Laboratorio, on_delete=models.SET_NULL, null=True)
    curso = models.ForeignKey(Curso, on_delete=models.SET_NULL, null=True)
    disciplina = models.ForeignKey(Disciplina, on_delete=models.SET_NULL, null=True)
    professor = models.ForeignKey(Professor, on_delete=models.SET_NULL, null=True)

    def name(self):
        return str(self.curso) + ' - ' + str(self.disciplina)

class Emprestimo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date = models.DateField()
    evento = models.CharField(max_length=200)
    responsavel = models.CharField(max_length=100)
    email = models.EmailField()
    contato = models.CharField(max_length=15, blank=True)
    computador = models.ForeignKey(Computador, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(accounts_models.CustomUsuario, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.evento

class SolicitacaoReserva(models.Model):
    
    STATUS_CHOICES = [
        ('P', 'Pendente'),
        ('F', 'Finalizada'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    observacao = models.TextField(blank=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=1, default='P')
    qnt_alunos = models.IntegerField()
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE)
    software = models.ManyToManyField(Software)
    user = models.ForeignKey(accounts_models.CustomUsuario, on_delete=models.CASCADE)

class RespostaSolicitacao(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    solicitacao = models.ForeignKey(SolicitacaoReserva, on_delete=models.CASCADE)
    resposta = models.TextField()
    user = models.ForeignKey(accounts_models.CustomUsuario, on_delete=models.CASCADE)

class Log(models.Model):

    CATEGORIA_CHOICES = [
        ('MN', 'Manutenção'),
        ('AT', 'Atualização'),
        ('IT', 'Instalação'),
        ('CR', 'Cadastro'),
        ('RV', 'Reserva'),
        ('EM', 'Empréstimo'),
        ('AS', 'Atualização Status'),
        ('NS', 'Nova Solicitação'),
    ]

    date = models.DateTimeField(auto_now_add=True)
    categoria = models.CharField(choices=CATEGORIA_CHOICES, max_length=2)
    laboratorio = models.ForeignKey(Laboratorio, on_delete=models.SET_NULL, null=True, blank=True)
    computador = models.ForeignKey(Computador, on_delete=models.SET_NULL, null=True, blank=True)
    reserva = models.ForeignKey(Reserva, on_delete=models.SET_NULL, null=True, blank=True)
    emprestimo = models.ForeignKey(Emprestimo, on_delete=models.SET_NULL, null=True, blank=True)
    software = models.ForeignKey(Software, on_delete=models.SET_NULL, null=True, blank=True)
    solicitacao = models.ForeignKey(SolicitacaoReserva, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(accounts_models.CustomUsuario, on_delete=models.SET_NULL, null=True)

class Manutencao(models.Model):
    STATUS_CHOICES = [
        ('Em Curso', 'Em Curso'),
        ('Resolvido', 'Resolvido'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    status = models.CharField(choices=STATUS_CHOICES, max_length=9, default='Em Curso')
    pc_codigo = models.ForeignKey(Computador, on_delete=models.SET_NULL, null=True, blank=True)
    data_inicio = models.DateField(auto_now_add=True)
    data_fim = models.DateField(null=True, blank=True)
    descricao = models.TextField(null=True, blank=True)
    user = models.ForeignKey(accounts_models.CustomUsuario, on_delete=models.SET_NULL, null=True, blank=True)
