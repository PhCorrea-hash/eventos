from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Define o módulo de configuração do Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')

app = Celery('setup')

# Usando a configuração do Django para o Celery
app.config_from_object('django.conf:settings', namespace='CELERY')

# Carrega as tarefas do Django
app.autodiscover_tasks()