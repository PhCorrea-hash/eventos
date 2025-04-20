from django.urls import path
from minhaArea.views import area
from eventos.views import eventos_view

urlpatterns = [
    path('area/', eventos_view, name='area'),
]