# Generated by Django 5.2 on 2025-05-15 17:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventos', '0014_ingresso_quantidade_disponivel'),
        ('perfil', '0003_alter_perfil_foto_perfil'),
    ]

    operations = [
        migrations.CreateModel(
            name='Carrinho',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantidade', models.PositiveIntegerField(default=1)),
                ('adicionado_em', models.DateTimeField(auto_now_add=True)),
                ('ingresso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eventos.ingresso')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='carrinho', to='perfil.perfil')),
            ],
        ),
    ]
