from django.db import models
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User

# Modelo de eventos para o db
class Eventos(models.Model):
    nome = models.CharField(max_length=150)
    legenda = models.CharField(max_length=150, null=False, default='')
    descricao = models.TextField()
    data = models.DateTimeField()
    local = models.CharField(max_length=150)
    imagem = CloudinaryField('image', null=True, blank=True)
    link = models.URLField(blank=True, null=True, default='')
    publicada = models.BooleanField(default=False)
    destaque = models.BooleanField(default=False)

    favoritos = models.ManyToManyField(User, related_name='eventos_favoritados', blank=True)

    def __str__(self):
        return self.nome
