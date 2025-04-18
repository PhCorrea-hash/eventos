from django.core.management.base import BaseCommand
from django.utils import timezone
from eventos.models import Eventos

class Command(BaseCommand):
    help = 'Apaga eventos que passaram mais de 4h da data'

    def handle(self, *args, **kwargs):
        agora = timezone.now()
        limite = agora - timezone.timedelta(hours=4)
        eventos_apagados, _ = Eventos.objects.filter(data__lt=limite).delete()
        self.stdout.write(self.style.SUCCESS(f'{eventos_apagados} eventos apagados.'))