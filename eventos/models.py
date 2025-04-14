from django.db import models

class Eventos(models.Model):
    nome = models.CharField(max_length=150)
    legenda = models.CharField(max_length=150, null=False, default='')
    descricao = models.TextField()
    data = models.DateTimeField()
    local = models.CharField(max_length=150)
    imagem = models.ImageField(upload_to='media/fotos/%Y/%m/%d/', blank=True, null=True)
    publicada = models.BooleanField(default=False)

    def __str__(self):
        return self.nome
