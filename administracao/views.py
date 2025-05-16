from django.shortcuts import render, redirect
from .models import TermosCondicoes, PoliticaPrivacidade, PoliticaCookies, InformacoesConsumidor
from eventos.models import Carrinho, Perfil
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json
from decimal import Decimal
from administracao.utils import Payload

def termos_condicoes(request):
    termos = TermosCondicoes.objects.prefetch_related('topicos__descricoes').all()
    ultima_atualizacao = TermosCondicoes.objects.latest('data_atualizacao').data_atualizacao if termos else None
    return render(request, 'administracao/termos.html', {'termos': termos, 'ultima_atualizacao': ultima_atualizacao})

def politica_privacidade(request):
    politicas = PoliticaPrivacidade.objects.prefetch_related('topicos__descricoes').all()
    ultima_atualizacao = PoliticaPrivacidade.objects.latest('data_atualizacao').data_atualizacao if politicas else None
    return render(request, 'administracao/politica.html', {
        'politicas': politicas, 
        'ultima_atualizacao': ultima_atualizacao
        })

def politica_cookies(request):
    politicas = PoliticaCookies.objects.prefetch_related('topicos__descricoes').all()
    ultima_atualizacao = PoliticaCookies.objects.latest('data_atualizacao').data_atualizacao if politicas else None
    return render(request, 'administracao/cookies.html', {
        'politicas': politicas,
        'ultima_atualizacao': ultima_atualizacao
    })

def informacoes_consumidor(request):
    politicas = InformacoesConsumidor.objects.prefetch_related('topicos__descricoes').all()
    ultima_atualizacao = InformacoesConsumidor.objects.latest('data_atualizacao').data_atualizacao if politicas else None
    return render(request, 'administracao/informacoes_consumidor.html', {
        'politicas': politicas,
        'ultima_atualizacao': ultima_atualizacao
    })


def finalizar_compra(request):
    if request.method != "POST":
        return JsonResponse({"sucesso": False, "erro": "Método inválido."})

    if not request.user.is_authenticated:
        return JsonResponse({"sucesso": False, "erro": "Login necessário."})

    forma_pagamento = request.POST.get('forma_pagamento')

    if forma_pagamento == 'pix':
        try:
            perfil = Perfil.objects.get(user=request.user)
        except Perfil.DoesNotExist:
            return JsonResponse({"sucesso": False, "erro": "Perfil do usuário não encontrado."})

        itens_carrinho = Carrinho.objects.filter(usuario=perfil)
        total = (sum(item.ingresso.preco * item.quantidade for item in itens_carrinho)) 

        if total <= 0:
            return JsonResponse({"sucesso": False, "erro": "Carrinho vazio ou valor inválido."})

        chave_pix = "38455378840"
        nome_merchant = "Pedro"
        cidade_merchant = "Rio"
        referencia = "Sonart"

        payload_obj = Payload(nome_merchant, chave_pix, total, cidade_merchant, referencia)
        payload_obj.gerarPayload()
        caminho_qrcode = payload_obj.gerarQrCode()

        return JsonResponse({
            "sucesso": True,
            "qr_code_url": caminho_qrcode,
            "payload": payload_obj.payload_completa,
            "mensagem": "Use o QR code para pagar via PIX."
        })

    return JsonResponse({"sucesso": False, "erro": "Forma de pagamento inválida."})
    
def checkout(request):
    if not request.user.is_authenticated:
        return redirect("/login")

    perfil = request.user.perfil  # Acessa o perfil do usuário logado
    itens_carrinho = Carrinho.objects.filter(usuario=perfil)
    total = sum(item.ingresso.preco * item.quantidade for item in itens_carrinho)

    chave_pix = "38455378840"
    nome_merchant = "Pedro"
    cidade_merchant = "Rio"
    referencia = "Sonart"

    payload_obj = Payload(nome_merchant, chave_pix, total, cidade_merchant, referencia)
    payload_obj.gerarPayload()

    return render(request, "administracao/checkout.html", {
        "itens_carrinho": itens_carrinho, 
        "total": total,
        "payload": payload_obj.payload_completa,
        })




