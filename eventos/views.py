from django.shortcuts import render
from eventos.models import Eventos
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

def index(request):

    eventos = Eventos.objects.order_by("data").filter(publicada=True)
    eventos_destaque = Eventos.objects.filter(publicada=True).order_by('data')[:3]
    return render(request, 'index.html', {
        "cards": eventos, 
        "cards_destaque": eventos_destaque
                   })

@csrf_exempt
def cloudinary_webhook(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        # Aqui você pode verificar os dados recebidos e reagir a eles, por exemplo:
        if 'event' in data and data['event'] == 'resource_added':
            # Alguma ação, como forçar a atualização ou notificar o frontend
            print(f'Novo evento: {data}')
            # Faça o que for necessário, como atualizar os dados ou cache
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'failed'}, status=400)