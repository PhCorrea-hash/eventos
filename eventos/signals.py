from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Eventos

@receiver(post_save, sender=Eventos)
def evento_criado(sender, instance, created, **kwargs):
    if created:
        print(f"Novo evento criado: {instance.nome}")
        # Aqui você pode colocar a lógica pra sincronizar com a API, etc.