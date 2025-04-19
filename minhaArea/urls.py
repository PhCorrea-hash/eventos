from django.urls import path
from minhaArea.views import area

urlpatterns = [
    path('area', area, name='area'),
]