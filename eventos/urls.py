from django.urls import path
from eventos.views import index
from . import views

urlpatterns = [
    path('', index, name='index'),
    path('webhook/cloudinary/', views.cloudinary_webhook, name='cloudinary-webhook'),
     path('api/eventos/', views.eventos_api, name='eventos_api'),
]