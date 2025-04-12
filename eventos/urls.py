from django.urls import path
from eventos.views import index

urlpatterns = [
    path('', index, name='index'),
]