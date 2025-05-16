from django.contrib import admin
from eventos.models import Eventos, Ingresso, Carrinho

class IngressoInline(admin.TabularInline):
    model = Ingresso
    extra = 1  
    min_num = 1  
    max_num = 10  

class ListandoEventos(admin.ModelAdmin):
    list_display = ("nome", "local", "publicada", "destaque")
    search_fields = ("nome", "local")
    list_filter = ("local",)
    list_editable = ("publicada", "destaque")
    inlines = [IngressoInline]

admin.site.register(Eventos, ListandoEventos)

admin.site.register(Ingresso)

admin.site.register(Carrinho)



