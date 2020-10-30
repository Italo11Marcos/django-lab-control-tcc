# Generated by Django 3.1.1 on 2020-10-29 13:22

import core.models
from django.conf import settings
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUsuario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='E-mail')),
                ('masp', models.CharField(max_length=15)),
                ('is_staff', models.BooleanField(default=False, verbose_name='Membro da equipe')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', core.models.UsuarioManager()),
            ],
        ),
        migrations.CreateModel(
            name='Computador',
            fields=[
                ('codigo', models.IntegerField(primary_key=True, serialize=False)),
                ('patrimonio', models.CharField(max_length=15)),
                ('dual_boot', models.BooleanField(default=False)),
                ('funciona', models.BooleanField(default=True)),
                ('processador', models.CharField(choices=[('I2', 'Intel Core 2 Duo'), ('I3', 'Intel I3'), ('I5', 'Intel I5'), ('IP', 'Intel Pentium Dual Core')], max_length=2)),
                ('hd', models.CharField(choices=[('100GB', '100GB'), ('200GB', '200GB'), ('300GB', '300GB'), ('400GB', '400GB'), ('500GB', '500GB')], max_length=5)),
                ('ram', models.CharField(choices=[('1GB', '1GB'), ('2GB', '2GB'), ('3GB', '3GB'), ('4GB', '4GB')], max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name='Curso',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45)),
            ],
        ),
        migrations.CreateModel(
            name='Disciplina',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=70)),
            ],
        ),
        migrations.CreateModel(
            name='Emprestimo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('evento', models.CharField(max_length=200)),
                ('responsavel', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('contato', models.CharField(blank=True, max_length=15)),
                ('computador_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.computador')),
                ('user_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Laboratorio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45)),
                ('qnt_computador', models.IntegerField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Professor',
            fields=[
                ('masp', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=150)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('contato', models.CharField(blank=True, max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='Software',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('versao', models.CharField(max_length=15)),
                ('tipo', models.CharField(choices=[('SL', 'Software Livre'), ('SP', 'Software Licenciado')], default='SL', max_length=2)),
                ('descricao', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='SolicitacaoReserva',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('observacao', models.TextField(null=True)),
                ('status', models.CharField(choices=[('P', 'Pendente'), ('F', 'Finzalizada')], default='P', max_length=1)),
                ('qnt_alunos', models.IntegerField()),
                ('curso_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.curso')),
                ('disciplina_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.disciplina')),
                ('professor_masp', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.professor')),
                ('software_id', models.ManyToManyField(to='core.Software')),
                ('user_masp', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RespostaSolicitacao',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('resposta', models.TextField()),
                ('solicitacao', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.solicitacaoreserva')),
                ('user_masp', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Reserva',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('evento', models.CharField(max_length=100)),
                ('responsavel', models.CharField(max_length=100)),
                ('contato', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=254)),
                ('start_day', models.DateField()),
                ('end_day', models.DateField()),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('curso_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.curso')),
                ('disciplina_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.disciplina')),
                ('laboratorio_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.laboratorio')),
                ('professor_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.professor')),
            ],
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('categoria', models.CharField(choices=[('MN', 'Manutenção'), ('AT', 'Atualização'), ('IT', 'Instalação'), ('CR', 'Criação'), ('RV', 'Reserva'), ('EM', 'Empréstimo'), ('AS', 'Atualização Status'), ('NS', 'Nova Solicitação')], max_length=2)),
                ('computador_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.computador')),
                ('emprestimo_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.emprestimo')),
                ('laboratorio_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.laboratorio')),
                ('reserva_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.reserva')),
                ('software_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.software')),
                ('solicitacao_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.solicitacaoreserva')),
                ('user_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='computador',
            name='laboratorio_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.laboratorio'),
        ),
        migrations.AddField(
            model_name='computador',
            name='software_id',
            field=models.ManyToManyField(to='core.Software'),
        ),
        migrations.CreateModel(
            name='Aula',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dia', models.CharField(choices=[('1', 'Segunda'), ('2', 'Terça'), ('3', 'Quarta'), ('4', 'Quinta'), ('5', 'Sexta'), ('6', 'Sabado'), ('7', 'Domingo')], max_length=1)),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('start_day', models.DateField()),
                ('end_day', models.DateField()),
                ('curso_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.curso')),
                ('disciplina_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.disciplina')),
                ('laboratorio_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.laboratorio')),
                ('professor_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.professor')),
            ],
        ),
    ]
