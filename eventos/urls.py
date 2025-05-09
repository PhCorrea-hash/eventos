from django.urls import path
from eventos.views import index, buscar_eventos, favoritar_evento, detalhes_evento
from . import views

# Urls do app eventos
urlpatterns = [
    path('', index, name='index'),
    path('webhook/cloudinary/', views.cloudinary_webhook, name='cloudinary-webhook'),
    path('api/eventos/', views.eventos_api, name='eventos_api'),
    path('buscar/', buscar_eventos, name='buscar_eventos'),
    path('favoritar/<int:evento_id>/', favoritar_evento, name='favoritar_evento'),
    path('<int:evento_id>/', detalhes_evento, name='detalhes_eventos'),
]