from django.db import models
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User

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

    def __str__(self):
        return self.nome

class Favorito(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    evento = models.ForeignKey(Eventos, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True,)

    class Meta:
        unique_together = ('user', 'evento')  # impede duplicação

    def __str__(self):
        return f'{self.user.username} - {self.evento.nome}'