# Generated by Django 3.1.1 on 2020-11-17 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20201117_0910'),
    ]

    operations = [
        migrations.RenameField(
            model_name='manutencao',
            old_name='user_id',
            new_name='user_masp',
        ),
        migrations.AlterField(
            model_name='manutencao',
            name='data_fim',
            field=models.DateField(blank=True),
        ),
        migrations.AlterField(
            model_name='manutencao',
            name='descricao',
            field=models.TextField(blank=True),
        ),
    ]
