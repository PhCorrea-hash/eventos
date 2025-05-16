from django.contrib.auth.models import User
from django.db import models
from cloudinary.models import CloudinaryField

class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="perfil")
    endereco = models.CharField(max_length=255, blank=True, null=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    data_nascimento = models.DateField(blank=True, null=True)
    foto_perfil = CloudinaryField('imagem', blank=True, default='default.png')

    def __str__(self):
        return self.user.username

    @property
    def nome(self):
        return self.user.first_name

    @property
    def email(self):
        return self.user.email

    @property
    def username(self):
        return self.user.username


class Ingresso(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    evento = models.ForeignKey('eventos.Eventos', on_delete=models.CASCADE)
    data_compra = models.DateTimeField(auto_now_add=True)
    codigo_ingresso = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"Ingresso de {self.usuario.username} para {self.evento.nome}"


class Pagamento(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data_pagamento = models.DateTimeField(auto_now_add=True)
    metodo_pagamento = models.CharField(max_length=50)

    def __str__(self):
        return f"Pagamento de {self.usuario.username} - R${self.valor}"
