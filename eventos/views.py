from django.shortcuts import render
from eventos.models import Eventos

def index(request):

    eventos = Eventos.objects.order_by("data").filter(publicada=True)
    eventos_destaque = Eventos.objects.filter(publicada=True).order_by('data')[:3]
    return render(request, 'index.html', {
        "cards": eventos, 
        "cards_destaque": eventos_destaque
                   })
