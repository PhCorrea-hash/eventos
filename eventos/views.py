from django.shortcuts import render
from eventos.models import Eventos, Favorito
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.db.models import Q
from django.utils.timezone import localtime
from django.utils import timezone
import unicodedata
from django.contrib.auth.decorators import login_required

def index(request):
    agora = timezone.now()
    limite = agora - timezone.timedelta(hours=4)

    # Exclui eventos que passaram mais de 4 horas
    Eventos.objects.filter(data__lt=limite).delete()

    eventos = Eventos.objects.order_by("data").filter(publicada=True)
    eventos_destaque = Eventos.objects.filter(publicada=True, destaque=True).order_by('data')[:3]

    return render(request, 'index.html', {
        "cards": eventos, 
        "cards_destaque": eventos_destaque
    })

def cloudinary_webhook(request):
    if request.method == 'POST':
        # Lógica para processar os dados do webhook
        # Você pode acessar os dados do webhook com request.body ou request.POST
        # Por exemplo:
        data = request.body
        print("Webhook recebido:", data)

        # Responda com um status HTTP 200 (OK)
        return JsonResponse({'status': 'ok'}, status=200)

    # Se o método não for POST, retornar um erro
    return JsonResponse({'error': 'Método não permitido'}, status=405)

def eventos_api(request):
    eventos = Eventos.objects.all().values('nome', 'descricao', 'imagem')
    data = [
        {
            'nome': e['nome'],
            'descricao': e['descricao'],
            'imagem': request.build_absolute_uri(e['imagem']),
        }
        for e in eventos
    ]
    return JsonResponse(data, safe=False)

def remover_acentos(txt):
    return ''.join(
        c for c in unicodedata.normalize('NFD', txt)
        if unicodedata.category(c) != 'Mn'
    )

def buscar_eventos(request):
    termo = request.GET.get('q', '').strip()
    termo_normalizado = remover_acentos(termo).lower()
    
    resultados = Eventos.objects.filter(publicada=True)

    eventos_filtrados = []
    for evento in resultados:
        nome_normalizado = remover_acentos(evento.nome).lower()
        descricao_normalizada = remover_acentos(evento.descricao).lower()
        legenda_normalizada = remover_acentos(evento.legenda or '').lower()


        if (termo_normalizado in nome_normalizado or termo_normalizado in descricao_normalizada or termo_normalizado in legenda_normalizada):
            eventos_filtrados.append(evento)

    data = []
    for evento in eventos_filtrados:
        data.append({
            'nome': evento.nome,
            'descricao': evento.descricao,
            'legenda': evento.legenda,
            'data': localtime(evento.data).strftime('%d/%m/%Y'),
            'link': evento.link,
            'imagem': evento.imagem.url if evento.imagem else '',
        })

    return JsonResponse(data, safe=False)

def favoritar_evento(request, evento_id):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Você precisa estar logado para favoritar um evento.'}, status=401)

    try:
        evento = Eventos.objects.get(id=evento_id)
    except Eventos.DoesNotExist:
        return JsonResponse({'error': 'Evento não encontrado.'}, status=404)

    favorito, created = Favorito.objects.get_or_create(user=request.user, evento=evento)

    if not created:
        favorito.delete()
        is_favorited = False
    else:
        is_favorited = True

    return JsonResponse({'favorited': is_favorited})
