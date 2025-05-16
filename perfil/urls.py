from django.urls import path
from perfil.views import perfil_view, editar_foto_perfil

urlpatterns = [
    path('perfil/', perfil_view, name='perfil'),
    path('editar-foto/', editar_foto_perfil, name='editar_foto_perfil'),
]