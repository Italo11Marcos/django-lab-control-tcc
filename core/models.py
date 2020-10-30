from django.db import models
import uuid, random
from django.contrib.auth.models import AbstractUser, BaseUserManager #AbstractBaseUser - bem básico

class UsuarioManager(BaseUserManager):

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('O e-mail é obrigatório')
        email = self.normalize_email(email)
        user = self.model(email=email, username=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        # extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser precisa ter is_superuser=True')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser precisa ter is_staff=True')

        return self._create_user(email, password, **extra_fields)


class CustomUsuario(AbstractUser):
    email = models.EmailField('E-mail', unique=True)
    masp = models.CharField(max_length=15)
    is_staff = models.BooleanField('Membro da equipe', default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'masp']

    def __str__(self):
        return self.email

    objects = UsuarioManager()

class Curso(models.Model):
    name = models.CharField(max_length=45)

    def __str__(self):
        return self.name

class Disciplina(models.Model):
    name = models.CharField(max_length=70)

    def __str__(self):
        return self.name

class Professor(models.Model):
    masp = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    contato = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return self.name

class Laboratorio(models.Model):
    name = models.CharField(max_length=45)
    qnt_computador = models.IntegerField(blank=True)

    def __str__(self):
        return self.name

class Software(models.Model):

    TIPO_CHOICES = [
        ('SL', 'Software Livre'),
        ('SP', 'Software Licenciado'),
    ]

    name = models.CharField(max_length=100)
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
    patrimonio = models.CharField(max_length=15)
    dual_boot = models.BooleanField(default=False)
    funciona = models.BooleanField(default=True)
    processador = models.CharField(choices=PROCESSADOR_CHOICES, max_length=2)
    hd = models.CharField(choices=HD_CHOICES, max_length=5)
    ram = models.CharField(choices=RAM_CHOICES, max_length=3)
    laboratorio_id = models.ForeignKey(Laboratorio, on_delete=models.SET_NULL, null=True)
    software_id = models.ManyToManyField(Software)

    def __str__(self):
        return str(self.codigo)

class Reserva(models.Model):
    #dia = models.DateField()
    evento = models.CharField(max_length=100)
    responsavel = models.CharField(max_length=100)
    contato = models.CharField(max_length=15)
    email = models.EmailField()
    start_day = models.DateField()
    end_day = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    laboratorio_id = models.ForeignKey(Laboratorio, on_delete=models.SET_NULL, null=True, blank=True)
    curso_id = models.ForeignKey(Curso, on_delete=models.SET_NULL, null=True, blank=True)
    disciplina_id = models.ForeignKey(Disciplina, on_delete=models.SET_NULL, null=True, blank=True)
    professor_id = models.ForeignKey(Professor, on_delete=models.SET_NULL, null=True, blank=True)
    #user_id = models.ForeignKey(CustomUsuario, on_delete=models.SET_NULL, null=True)

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

    dia = models.CharField(choices=DIA_CHOICES, max_length=1)
    start_time = models.TimeField()
    end_time = models.TimeField()
    start_day = models.DateField()
    end_day = models.DateField()
    laboratorio_id = models.ForeignKey(Laboratorio, on_delete=models.SET_NULL, null=True)
    curso_id = models.ForeignKey(Curso, on_delete=models.SET_NULL, null=True)
    disciplina_id = models.ForeignKey(Disciplina, on_delete=models.SET_NULL, null=True)
    professor_id = models.ForeignKey(Professor, on_delete=models.SET_NULL, null=True)

    def name(self):
        return str(self.curso_id) + ' ' + str(self.disciplina_id)

class Emprestimo(models.Model):
    date = models.DateTimeField()
    evento = models.CharField(max_length=200)
    responsavel = models.CharField(max_length=100)
    email = models.EmailField()
    contato = models.CharField(max_length=15, blank=True)
    computador_codigo = models.ForeignKey(Computador, on_delete=models.SET_NULL, null=True)
    user_id = models.ForeignKey(CustomUsuario, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.evento

class SolicitacaoReserva(models.Model):
    
    STATUS_CHOICES = [
        ('P', 'Pendente'),
        ('F', 'Finzalizada'),
    ]

    observacao = models.TextField(null=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=1, default='P')
    qnt_alunos = models.IntegerField()
    professor_masp = models.ForeignKey(Professor, on_delete=models.CASCADE)
    curso_id = models.ForeignKey(Curso, on_delete=models.CASCADE)
    disciplina_id = models.ForeignKey(Disciplina, on_delete=models.CASCADE)
    software_id = models.ManyToManyField(Software)
    user_masp = models.ForeignKey(CustomUsuario, on_delete=models.CASCADE)

class RespostaSolicitacao(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    solicitacao = models.ForeignKey(SolicitacaoReserva, on_delete=models.CASCADE)
    resposta = models.TextField()
    user_masp = models.ForeignKey(CustomUsuario, on_delete=models.CASCADE)

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
    laboratorio_id = models.ForeignKey(Laboratorio, on_delete=models.SET_NULL, null=True, blank=True)
    computador_id = models.ForeignKey(Computador, on_delete=models.SET_NULL, null=True, blank=True)
    reserva_id = models.ForeignKey(Reserva, on_delete=models.SET_NULL, null=True, blank=True)
    emprestimo_id = models.ForeignKey(Emprestimo, on_delete=models.SET_NULL, null=True, blank=True)
    software_id = models.ForeignKey(Software, on_delete=models.SET_NULL, null=True, blank=True)
    solicitacao_id = models.ForeignKey(SolicitacaoReserva, on_delete=models.SET_NULL, null=True)
    user_id = models.ForeignKey(CustomUsuario, on_delete=models.SET_NULL, null=True)