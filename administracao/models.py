from django.db import models

class TermosCondicoes(models.Model):
    titulo = models.CharField(max_length=150)
    data_atualizacao = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titulo
    
class TermoItem(models.Model):
    termos = models.ForeignKey(TermosCondicoes, related_name="topicos", on_delete=models.CASCADE)
    titulo = models.CharField(max_length=255)

    def __str__(self):
        return self.titulo

class Descricao(models.Model):
    termo = models.ForeignKey(TermoItem, related_name="descricoes", on_delete=models.CASCADE)
    conteudo = models.TextField()

    def __str__(self):
        return f"Descrição para {self.termo.titulo}"

# Politica de privacidade
class PoliticaPrivacidade(models.Model):
    titulo = models.CharField(max_length=150)
    data_atualizacao = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titulo
    
class PoliticaItem(models.Model):
    politica = models.ForeignKey(PoliticaPrivacidade, related_name="topicos", on_delete=models.CASCADE)
    titulo = models.CharField(max_length=255)

    def __str__(self):
        return self.titulo

class PoliticaDescricao(models.Model):
    item = models.ForeignKey(PoliticaItem, related_name="descricoes", on_delete=models.CASCADE)
    conteudo = models.TextField()

    def __str__(self):
        return f"Descrição para {self.item.titulo}"
    
# Política de cookies
class PoliticaCookies(models.Model):
    titulo = models.CharField(max_length=150)
    data_atualizacao = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titulo
    
class CookieItem(models.Model):
    politica = models.ForeignKey(PoliticaCookies, related_name="topicos", on_delete=models.CASCADE)
    titulo = models.CharField(max_length=255)

    def __str__(self):
        return self.titulo

class CookieDescricao(models.Model):
    item = models.ForeignKey(CookieItem, related_name="descricoes", on_delete=models.CASCADE)
    conteudo = models.TextField()

    def __str__(self):
        return f"Descrição para {self.item.titulo}"
    
#Informações ao consumidor
class InformacoesConsumidor(models.Model):
    titulo = models.CharField(max_length=150)
    data_atualizacao = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titulo
    
class ConsumidorItem(models.Model):
    politica = models.ForeignKey(InformacoesConsumidor, related_name="topicos", on_delete=models.CASCADE)
    titulo = models.CharField(max_length=255)

    def __str__(self):
        return self.titulo

class ConsumidorDescricao(models.Model):
    item = models.ForeignKey(ConsumidorItem, related_name="descricoes", on_delete=models.CASCADE)
    conteudo = models.TextField()

    def __str__(self):
        return f"Descrição para {self.item.titulo}"

