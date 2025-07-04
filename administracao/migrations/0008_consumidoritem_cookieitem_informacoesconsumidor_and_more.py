# Generated by Django 5.2 on 2025-05-15 04:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administracao', '0007_remove_politicaprivacidade_conteudo_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConsumidorItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='CookieItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='InformacoesConsumidor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=150)),
                ('data_atualizacao', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='PoliticaCookies',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=150)),
                ('data_atualizacao', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='ConsumidorDescricao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('conteudo', models.TextField()),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='descricoes', to='administracao.consumidoritem')),
            ],
        ),
        migrations.CreateModel(
            name='CookieDescricao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('conteudo', models.TextField()),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='descricoes', to='administracao.cookieitem')),
            ],
        ),
        migrations.AddField(
            model_name='consumidoritem',
            name='politica',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='topicos', to='administracao.informacoesconsumidor'),
        ),
        migrations.AddField(
            model_name='cookieitem',
            name='politica',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='topicos', to='administracao.politicacookies'),
        ),
    ]
