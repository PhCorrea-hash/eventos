from django.shortcuts import render
from eventos.models import Eventos

def index(request):

    eventos = Eventos.objects.order_by("data").filter(publicada=True)
    return render(request, 'index.html', {"cards": eventos})
