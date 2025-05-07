from django.shortcuts import render, get_object_or_404
from eventos.models import Eventos
from django.http import JsonResponse
from django.utils.timezone import localtime
from django.utils import timezone
import unicodedata
from django.contrib.auth.decorators import login_required

# Renderizar a página principal
def index(request):
    agora = timezone.now()
    limite = agora - timezone.timedelta(hours=4)

    # Exclui eventos que passaram mais de 4 horas
    Eventos.objects.filter(data__lt=limite).delete()

    eventos = Eventos.objects.order_by("data").filter(publicada=True)
    eventos_destaque = Eventos.objects.filter(publicada=True, destaque=True).order_by('data')[:3]

    favoritos_ids = []
    if request.user.is_authenticated:
        favoritos_ids = request.user.eventos_favoritados.values_list('id', flat=True)

    return render(request, 'index.html', {
        "cards": eventos, 
        "cards_destaque": eventos_destaque,
        "favoritos_ids": favoritos_ids
    })

# Conectar com o cloudinary
def cloudinary_webhook(request):
    if request.method == 'POST':
        
        data = request.body
        print("Webhook recebido:", data)

        # Resposta com um status HTTP 200 (OK)
        return JsonResponse({'status': 'ok'}, status=200)

    # Se o método não for POST, retornar um erro
    return JsonResponse({'error': 'Método não permitido'}, status=405)

# Api para buscar eventos na web (em desenvolvimento)
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

# Função para remover os acentos do input da busca de eventos
def remover_acentos(txt):
    return ''.join(
        c for c in unicodedata.normalize('NFD', txt)
        if unicodedata.category(c) != 'Mn'
    )

# Fubção para buscar eventos
def buscar_eventos(request):
    termo = request.GET.get('q', '').strip()
    termo_normalizado = remover_acentos(termo).lower()
    usuario = request.user

    # Busca todos os eventos
    resultados = Eventos.objects.filter(publicada=True)

    eventos_filtrados = []
    for evento in resultados:
        nome_normalizado = remover_acentos(evento.nome).lower()
        descricao_normalizada = remover_acentos(evento.descricao).lower()
        legenda_normalizada = remover_acentos(evento.legenda or '').lower()

        if termo_normalizado in nome_normalizado or termo_normalizado in legenda_normalizada:
            # Verifica se o evento é favorito para o usuário atual
            favorito = evento.favoritos.filter(id=usuario.id).exists() if usuario.is_authenticated else False

            eventos_filtrados.append({
                'id': evento.id,
                'nome': evento.nome,
                'descricao': evento.descricao,
                'legenda': evento.legenda,
                'data': localtime(evento.data).strftime('%d/%m/%Y'),
                'link': evento.link,
                'imagem': evento.imagem.url if evento.imagem else '',
                'favorito': favorito,
            })

    return JsonResponse(eventos_filtrados, safe=False)

# Função para favoritar os eventos
@login_required
def favoritar_evento(request, evento_id):
    evento = get_object_or_404(Eventos, id=evento_id)
    user = request.user

    if user in evento.favoritos.all():
        evento.favoritos.remove(user)
        favoritado = False
    else:
        evento.favoritos.add(user)
        favoritado = True

    return JsonResponse({'favorited': favoritado})

# Função para renderizar os eventos favoritados na página area.html
@login_required
def eventos_view(request):
    user = request.user
    
    # Busca todos os eventos
    eventos = Eventos.objects.all()
    
    # Busca apenas os IDs dos eventos que o usuário favoritou
    favoritos_ids = user.eventos_favoritados.values_list('id', flat=True)

    return render(request, 'minhaArea/area.html', {
        'eventos': eventos,
        'favoritos_ids': list(favoritos_ids),
    })

# Função para renderizar a página de detalhes do evento
def detalhes_evento(request, evento_id):
    evento = get_object_or_404(Eventos, id=evento_id)
    return render(request, 'eventos/detalhes_eventos.html', {'evento': evento})