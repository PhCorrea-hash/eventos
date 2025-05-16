from django.shortcuts import render, get_object_or_404, redirect
from eventos.models import Eventos, Ingresso, Carrinho
from perfil.models import Perfil
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

    eventos = Eventos.objects.filter(publicada=True).order_by('-promovido_no_site', 'data')
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
    ingressos = evento.ingressos.all()

    carrinho_itens = {}
    if request.user.is_authenticated:
        perfil = Perfil.objects.get(user=request.user)
        carrinho = Carrinho.objects.filter(usuario=perfil, ingresso__in=ingressos)
        for item in carrinho:
            carrinho_itens[item.ingresso.id] = item.quantidade

    itens_carrinho = Carrinho.objects.filter(usuario=perfil)
    quantidades_carrinho = {item.ingresso.id: item.quantidade for item in itens_carrinho}
    total = sum(item.ingresso.preco * item.quantidade for item in itens_carrinho)

    # Enviar para o template
    context = {
        "evento": evento,
        "ingressos": ingressos,
        "quantidades_carrinho": carrinho_itens,
        "total_carrinho": f"{total:.2f}",
    }
    return render(request, "eventos/detalhes_eventos.html", context)

def sobre(request):
    return render(request, 'sobre/sobre.html')

# def adicionar_ao_carrinho(request, ingresso_id):
#     if request.user.is_authenticated:
#         perfil = Perfil.objects.get(user=request.user)
#         ingresso = get_object_or_404(Ingresso, id=ingresso_id)

#         # Pega a quantidade da query string
#         quantidade = int(request.GET.get('quantidade', 1))

#         # Verifica se há ingressos suficientes
#         if ingresso.quantidade_disponivel >= quantidade:
#             # Cria ou atualiza o item no carrinho
#             item, created = Carrinho.objects.get_or_create(usuario=perfil, ingresso=ingresso)

#             # Corrige a lógica para evitar o salto na quantidade
#             if created:
#                 item.quantidade = quantidade
#             else:
#                 item.quantidade += quantidade

#             item.save()

#             # Atualiza o estoque
#             ingresso.quantidade_disponivel -= quantidade
#             ingresso.save()

#             return JsonResponse({"sucesso": True})
#         else:
#             return JsonResponse({"sucesso": False, "erro": "Quantidade insuficiente em estoque."})
#     else:
#         return JsonResponse({"sucesso": False, "erro": "Você precisa estar logado para adicionar ingressos ao carrinho."})
    
# def remover_do_carrinho(request, item_id):
#     if request.user.is_authenticated:
#         item = get_object_or_404(Carrinho, id=item_id)
#         if item.usuario.user == request.user:
#             # Devolve o estoque ao remover do carrinho
#             item.ingresso.quantidade_disponivel += item.quantidade
#             item.ingresso.save()
#             item.delete()
#     return redirect('detalhes_eventos', item.ingresso.evento.id)

def adicionar_ao_carrinho(request, ingresso_id):
    if not request.user.is_authenticated:
        return JsonResponse({"sucesso": False, "erro": "Login necessário."})
    
    perfil = Perfil.objects.get(user=request.user)
    ingresso = get_object_or_404(Ingresso, id=ingresso_id)

    if ingresso.quantidade_disponivel <= 0:
        return JsonResponse({"sucesso": False, "erro": "Sem ingressos disponíveis."})

    item, created = Carrinho.objects.get_or_create(usuario=perfil, ingresso=ingresso)

    # Só incrementa se não foi recém criado
    if not created:
        item.quantidade += 1
    
    item.save()

    total = sum(item.ingresso.preco * item.quantidade for item in Carrinho.objects.filter(usuario=perfil))

    ingresso.quantidade_disponivel -= 1
    ingresso.save()

    return JsonResponse({"sucesso": True, "quantidade": item.quantidade, "total": f"{total:.2f}"})

def remover_do_carrinho(request, ingresso_id):
    if not request.user.is_authenticated:
        return JsonResponse({"sucesso": False, "erro": "Login necessário."})

    perfil = Perfil.objects.get(user=request.user)
    ingresso = get_object_or_404(Ingresso, id=ingresso_id)

    # Verifica se o item está no carrinho
    if not Carrinho.objects.filter(usuario=perfil, ingresso=ingresso).exists():
        return JsonResponse({"sucesso": False, "erro": "Item não encontrado no carrinho."})

    # Remove ou decrementa a quantidade do ingresso
    item = Carrinho.objects.get(usuario=perfil, ingresso=ingresso)
    item.quantidade -= 1

    if item.quantidade <= 0:
        item.delete()
    else:
        item.save()

    # Libera o ingresso de volta ao estoque
    ingresso.quantidade_disponivel += 1
    ingresso.save()

    # Calcula o total do carrinho
    total = sum(i.ingresso.preco * i.quantidade for i in Carrinho.objects.filter(usuario=perfil))

    return JsonResponse({"sucesso": True, "quantidade": item.quantidade if item.pk else 0, "total": f"{total:.2f}"})
    
@login_required
def visualizar_carrinho(request):
    perfil = request.user.perfil  # Acessa o perfil do usuário logado
    itens_carrinho = Carrinho.objects.filter(usuario=perfil)
    total = sum(item.ingresso.preco * item.quantidade for item in itens_carrinho)
    return render(request, 'eventos/carrinho.html', {
        'itens_carrinho': itens_carrinho,
        'total': total
    })

@login_required
def finalizar_compra(request):
    perfil = request.user.perfil
    itens_carrinho = Carrinho.objects.filter(usuario=perfil)

    if not itens_carrinho.exists():
        return JsonResponse({'sucesso': False, 'mensagem': 'Seu carrinho está vazio.'})

    # Aqui você pode adicionar a lógica de pagamento e emissão de ingressos
    # Por enquanto, apenas limpa o carrinho após a compra
    itens_carrinho.delete()

    return JsonResponse({'sucesso': True, 'mensagem': 'Compra finalizada com sucesso!'})


def detalhes_carrinho(request):
    carrinho = request.session.get('carrinho', {})
    total = 0.0
    quantidades = {}

    # Calcule total e quantidades (exemplo simples)
    for ingresso_id, quantidade in carrinho.items():
        # Aqui você pode buscar o preço do ingresso no banco de dados
        # Exemplo rápido:
        from eventos.models import Ingresso
        try:
            ingresso = Ingresso.objects.get(pk=ingresso_id)
            total += ingresso.preco * quantidade
            quantidades[str(ingresso_id)] = quantidade
        except Ingresso.DoesNotExist:
            continue

    return JsonResponse({
        'total': total,
        'quantidades': quantidades,
    })