from django.db import models
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
        #extra_fields.setdefault('is_statff', True) Por padrão já é false
        extra_fields.setdefault('is_superuser', 'False')
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        return self._create_user(email, password, **extra_fields)

class CustomUsuario(AbstractUser):
    email = models.EmailField('E-mail', unique=True)
    masp = models.CharField(max_length=10)
    #is_staff = models.BooleanField('Membro da equipe', default=True)
    #Aqui eu poderia criar vários outros campos
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'masp']

    objects = UsuarioManager()

class Curso(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=45)

class Disciplina(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=70)

class Professor(models.Model):
    id = models.IntegerField(primary_key=True)
    masp = models.CharField(max_length=10)
    name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    contato = models.CharField(max_length=15, blank=True)

class Laboratorio(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=45)
    qnt_computador = models.IntegerField(blank=True)

class Software(models.Model):

    TIPO_CHOICES = [
        ('SL', 'Software Livre'),
        ('SP', 'Software Licenciado'),
    ]

    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    versao = models.CharField(max_length=15)
    tipo = models.CharField(choices=TIPO_CHOICES, max_length=2)
    descricao = models.TextField()

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

    codigo = models.CharField(max_length=15, primary_key=True)
    patrimonio = models.CharField(max_length=15)
    dual_boot = models.BooleanField(default=False)
    funciona = models.BooleanField(default=True)
    processador = models.CharField(choices=PROCESSADOR_CHOICES, max_length=2)
    hd = models.CharField(choices=HD_CHOICES, max_length=5)
    ram = models.CharField(choices=RAM_CHOICES, max_length=3)
    laboratorio_id = models.ForeignKey(Laboratorio, on_delete=models.SET_NULL, null=True)
    software_id = models.ManyToManyField(Software)

class Reserva(models.Model):
    id = models.IntegerField(primary_key=True)
    dia = models.DateField()
    horario_inicio = models.TimeField()
    horario_fim = models.TimeField()
    observacao = models.TextField(verbose_name='Observação')
    laboratorio_id = models.ForeignKey(Laboratorio, on_delete=models.SET_NULL, null=True)
    curso_id = models.ForeignKey(Curso, on_delete=models.SET_NULL, null=True)
    disciplina_id = models.ForeignKey(Disciplina, on_delete=models.SET_NULL, null=True)
    professor_id = models.ForeignKey(Professor, on_delete=models.SET_NULL, null=True)
    user_id = models.ForeignKey(CustomUsuario, on_delete=models.SET_NULL, null=True)

class Emprestimo(models.Model):
    id = models.IntegerField(primary_key=True)
    date = models.DateTimeField()
    evento = models.CharField(max_length=200)
    responsavel = models.CharField(max_length=100)
    email = models.EmailField()
    contato = models.CharField(max_length=15, blank=True)
    computador_id = models.ForeignKey(Computador, on_delete=models.SET_NULL, null=True)
    user_id = models.ForeignKey(CustomUsuario, on_delete=models.SET_NULL, null=True)

class Log(models.Model):

    CATEGORIA_CHOICES = [
        ('MN', 'Manutenção'),
        ('AT', 'Atualização'),
        ('IT', 'Instalação'),
        ('CR', 'Criação'),
        ('RV', 'Reserva'),
        ('EM', 'Empréstimo'),
    ]

    date = models.DateTimeField(auto_now_add=True)
    categoria = models.CharField(choices=CATEGORIA_CHOICES, max_length=2)
    laboratorio_id = models.ForeignKey(Laboratorio, on_delete=models.SET_NULL, null=True, blank=True)
    computador_id = models.ForeignKey(Computador, on_delete=models.SET_NULL, null=True, blank=True)
    reserva_id = models.ForeignKey(Reserva, on_delete=models.SET_NULL, null=True, blank=True)
    emprestimo_id = models.ForeignKey(Emprestimo, on_delete=models.SET_NULL, null=True, blank=True)
    software_id = models.ForeignKey(Software, on_delete=models.SET_NULL, null=True, blank=True)