from django.urls import path
from eventos.views import index, buscar_eventos, favoritar_evento
from . import views

urlpatterns = [
    path('', index, name='index'),
    path('webhook/cloudinary/', views.cloudinary_webhook, name='cloudinary-webhook'),
    path('api/eventos/', views.eventos_api, name='eventos_api'),
    path('buscar/', buscar_eventos, name='buscar_eventos'),
    path('favoritar/<int:evento_id>/', favoritar_evento, name='favoritar_evento'),
]