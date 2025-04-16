from __future__ import absolute_import, unicode_literals
from .celery import app as celery_app

__all__ = ('celery_app',)

# Isso garante que o Celery seja carregado quando o Django iniciar
