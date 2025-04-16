from django.urls import path
from eventos.views import index, buscar_eventos, webhook_importar_eventos
from . import views

urlpatterns = [
    path('', index, name='index'),
    path('webhook/cloudinary/', views.cloudinary_webhook, name='cloudinary-webhook'),
    path('api/eventos/', views.eventos_api, name='eventos_api'),
    path('buscar/', views.buscar_eventos, name='buscar_eventos'),
    path("webhook/importar-eventos/", webhook_importar_eventos),
]