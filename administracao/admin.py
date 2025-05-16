import nested_admin
from django.contrib import admin
from .models import TermosCondicoes, PoliticaPrivacidade, Descricao, TermoItem, PoliticaDescricao, PoliticaItem

class DescricaoInline(nested_admin.NestedTabularInline):
    model = Descricao
    extra = 1

class TermoItemInline(nested_admin.NestedTabularInline):
    model = TermoItem
    inlines = [DescricaoInline]
    extra = 1

@admin.register(TermosCondicoes)
class TermosCondicoesAdmin(nested_admin.NestedModelAdmin):
    inlines = [TermoItemInline]

class PoliticaDescricaoInline(nested_admin.NestedTabularInline):
    model = PoliticaDescricao
    extra = 1

class PoliticaItemInline(nested_admin.NestedTabularInline):
    model = PoliticaItem
    extra = 1
    inlines = [PoliticaDescricaoInline]

@admin.register(PoliticaPrivacidade)
class PoliticaPrivacidadeAdmin(nested_admin.NestedModelAdmin):
    inlines = [PoliticaItemInline]

# Política de cookies
from .models import PoliticaCookies, CookieItem, CookieDescricao

class CookieDescricaoInline(nested_admin.NestedTabularInline):
    model = CookieDescricao
    extra = 1

class CookieItemInline(nested_admin.NestedTabularInline):
    model = CookieItem
    extra = 1
    inlines = [CookieDescricaoInline]

@admin.register(PoliticaCookies)
class PoliticaCookiesAdmin(nested_admin.NestedModelAdmin):
    list_display = ('titulo', 'data_atualizacao')
    inlines = [CookieItemInline]

# Informações ao consumidor
from .models import InformacoesConsumidor, ConsumidorItem, ConsumidorDescricao

class ConsumidorDescricaoInline(nested_admin.NestedTabularInline):
    model = ConsumidorDescricao
    extra = 1

class ConsumidorItemInline(nested_admin.NestedTabularInline):
    model = ConsumidorItem
    extra = 1
    inlines = [ConsumidorDescricaoInline]

@admin.register(InformacoesConsumidor)
class InformacoesConsumidorAdmin(nested_admin.NestedModelAdmin):
    list_display = ('titulo', 'data_atualizacao')
    inlines = [ConsumidorItemInline]

