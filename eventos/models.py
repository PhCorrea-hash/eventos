from django.db import models
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User
from perfil.models import Perfil

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
    promovido_no_site = models.BooleanField(default=False)

    favoritos = models.ManyToManyField(User, related_name='eventos_favoritados', blank=True)

    def __str__(self):
        return self.nome
    
class Ingresso(models.Model):
    evento = models.ForeignKey(Eventos, on_delete=models.CASCADE, related_name='ingressos')
    tipo = models.CharField(max_length=100)
    preco = models.DecimalField(max_digits=8, decimal_places=2)
    quantidade_disponivel = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.tipo} - {self.evento.nome} - R$ {self.preco}"

    def vender_ingresso(self, quantidade=1):
        if self.quantidade_disponivel >= quantidade:
            self.quantidade_disponivel -= quantidade
            self.save()
            return True
        return False

class Carrinho(models.Model):
    usuario = models.ForeignKey(Perfil, on_delete=models.CASCADE, related_name='carrinho')
    ingresso = models.ForeignKey(Ingresso, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=1)
    adicionado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.user.username} - {self.ingresso} (x{self.quantidade})"

    def total(self):
        return self.quantidade * self.ingresso.preco