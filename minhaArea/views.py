from django.shortcuts import render
from eventos.models import Eventos, Favorito

def area(request):
    eventos = Eventos.objects.all()

    if request.user.is_authenticated:
        favoritos = Favorito.objects.filter(user=request.user)
        favoritos_ids = [favorito.evento.id for favorito in favoritos]
    else:
        favoritos_ids = []

    return render(request, 'minhaArea/area.html', {
        'eventos': eventos,
        'favoritos_ids': favoritos_ids,
    })
