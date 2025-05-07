from django.db import models
from django.contrib.auth.models import User
from eventos.models import Eventos

# Modelo de grupos para o db
class Grupo(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    membros = models.ManyToManyField(User, related_name='grupos')
    eventos = models.ManyToManyField('eventos.Eventos', blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome

# Modelo de compartilhar eventos no chat do grupo   
class EventoCompartilhado(models.Model):
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE, related_name='eventos_compartilhados')
    evento = models.ForeignKey(Eventos, on_delete=models.CASCADE)
    compartilhado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    data_compartilhamento = models.DateTimeField(auto_now_add=True)

# Modelo para enviar e salvar mensgaens no chat do grupo
class MensagemGrupo(models.Model):
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE, related_name='mensagens')
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    texto = models.TextField(null=True, blank=True)
    evento = models.ForeignKey(Eventos, on_delete=models.SET_NULL, null=True, blank=True)
    data_envio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Mensagem de {self.autor.username} no grupo {self.grupo.nome}"

# Modelo da agenda de eventos do usuário
class Agenda(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    evento = models.ForeignKey(Eventos, on_delete=models.CASCADE)
    data_adicao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.evento.nome}"
    