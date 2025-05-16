from django.urls import path
from eventos.views import index, buscar_eventos, favoritar_evento, detalhes_evento, sobre, adicionar_ao_carrinho, remover_do_carrinho, visualizar_carrinho, finalizar_compra, detalhes_carrinho
from . import views

# Urls do app eventos
urlpatterns = [
    path('', index, name='index'),
    path('webhook/cloudinary/', views.cloudinary_webhook, name='cloudinary-webhook'),
    path('api/eventos/', views.eventos_api, name='eventos_api'),
    path('buscar/', buscar_eventos, name='buscar_eventos'),
    path('favoritar/<int:evento_id>/', favoritar_evento, name='favoritar_evento'),
    path('<int:evento_id>/', detalhes_evento, name='detalhes_eventos'),
    path('sobre/', sobre, name='sobre'),
    path('adicionar_ao_carrinho/<int:ingresso_id>/', adicionar_ao_carrinho, name='adicionar_ao_carrinho'),
    path('remover_do_carrinho/<int:ingresso_id>/', remover_do_carrinho, name='remover_do_carrinho'),
    path('visualizar/', visualizar_carrinho, name='visualizar_carrinho'),
    path('finalizar/', finalizar_compra, name='finalizar_compra'),
    path('carrinho/detalhes/', detalhes_carrinho, name='detalhes_carrinho'),
]