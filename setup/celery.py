from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Define as configurações padrão do Django para o celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')

app = Celery('setup')

# Carrega configurações do settings.py com prefixo CELERY_
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-descobre tarefas nos apps instalados
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')