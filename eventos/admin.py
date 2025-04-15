from django.contrib import admin
from eventos.models import Eventos

class ListandoEventos(admin.ModelAdmin):
    list_display = ("nome", "local", "publicada", "destaque")
    search_fields = ("nome", "local")
    list_filter = ("local",)
    list_editable = ("publicada", "destaque")

admin.site.register(Eventos, ListandoEventos)
