from django.db import models


class Categoria(models.Model):
    nome = models.CharField(max_length=50)

    def __str__(self):
        return self.nome
    
class Livro(models.Model):
    streaming_choices = (('A', 'Amazon Klindle'), ('F', 'Físico'))
    nome = models.CharField(max_length=50)
    streaming = models.CharField(max_length=2, choices=streaming_choices)
    nota = models.IntegerField(null=True, blank=True)
    comentario = models.TextField(null=True, blank=True)
    categorias = models.ManyToManyField(Categoria)
    
    def __str__(self):
        return self.nome
