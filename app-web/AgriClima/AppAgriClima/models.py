from django.db import models

# Create your models here.
class Estacao(models.Model):
    codigo = models.CharField(max_length=100)
    nome = models.CharField(max_length=500)
    latitude = models.CharField(max_length=100)
    longitude = models.CharField(max_length=100)
    tipoEstacao = models.CharField(max_length=100)

    class Meta:
        app_label = 'AppAgriClima'

    def __str__(self):
        return self.nome