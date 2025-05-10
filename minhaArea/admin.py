from django.contrib import admin
from minhaArea.models import Agenda, Grupo, MensagemGrupo, EventoCompartilhado

class listandoAgenda(admin.ModelAdmin):
    list_display = ("evento", "data_evento")

admin.site.register(Agenda, listandoAgenda)

class listandoGrupos(admin.ModelAdmin):
    list_display = ("nome",)

admin.site.register(Grupo, listandoGrupos)

class listandoMensagens(admin.ModelAdmin):
    list_display = ("grupo",)

admin.site.register(MensagemGrupo, listandoMensagens)

class listandoEventosNoGrupo(admin.ModelAdmin):
    list_display = ("grupo",)

admin.site.register(EventoCompartilhado, listandoEventosNoGrupo)