from django.db import models
from django.contrib.auth.models import User
from eventos.models import Eventos

class Grupo(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    membros = models.ManyToManyField(User, related_name='grupos')
    eventos = models.ManyToManyField('eventos.Eventos', blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome
    
class EventoCompartilhado(models.Model):
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE, related_name='eventos_compartilhados')
    evento = models.ForeignKey(Eventos, on_delete=models.CASCADE)
    compartilhado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    data_compartilhamento = models.DateTimeField(auto_now_add=True)

class MensagemGrupo(models.Model):
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE, related_name='mensagens')
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    texto = models.TextField(null=True, blank=True)
    evento = models.ForeignKey(Eventos, on_delete=models.SET_NULL, null=True, blank=True)
    data_envio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Mensagem de {self.autor.username} no grupo {self.grupo.nome}"
    
class Agenda(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    evento = models.ForeignKey(Eventos, on_delete=models.CASCADE)
    data_adicao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.evento.nome}"
    
class GoogleCredentials(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    client_id = models.CharField(max_length=255)
    client_secret = models.CharField(max_length=255)
    refresh_token = models.CharField(max_length=255)
    access_token = models.CharField(max_length=255, blank=True, null=True)
    expires_in = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Google Credentials for {self.user.username}"

    def save(self, *args, **kwargs):
        # Lógica para atualizar ou criar as credenciais, se necessário.
        super(GoogleCredentials, self).save(*args, **kwargs)