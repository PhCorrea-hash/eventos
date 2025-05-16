from django.urls import path
from .views import termos_condicoes, politica_privacidade, politica_cookies, informacoes_consumidor, finalizar_compra, checkout
from eventos.views import detalhes_carrinho

urlpatterns = [
    path('termos/', termos_condicoes, name='termos'),
    path('politica/', politica_privacidade, name='politica'),
    path('politica-cookies/', politica_cookies, name='cookies'),
    path('informacoes-ao-consumidor/', informacoes_consumidor, name='info-ao-consumidor'),
    path('finalizar_compra/', finalizar_compra, name='finalizar_compra'),
    path('checkout/', checkout, name='checkout'),
    path('carrinho/detalhes/', detalhes_carrinho, name='detalhes_carrinho'),
]