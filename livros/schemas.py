from ninja import ModelSchema, Schema
from .models import Categoria, Livro


class LivroSchema(ModelSchema):
    class Meta:
        model = Livro
        fields = ['nome', 'streaming', 'categorias']


class AvaliacaoSchema(ModelSchema):
    class Meta:
        model = Livro
        fields = ['nota', 'comentario']


class FiltrosSortear(Schema):
    nota_minima: int = None
    categoria: int = None
    lido: bool = False


class LivrosViewSchema(ModelSchema):
    class Meta:
        model = Livro
        fields = ['nome', 'nota', 'categorias', 'id']


class CategoriasViewSchema(ModelSchema):
    class Meta:
        model = Categoria
        fields = ['nome']
