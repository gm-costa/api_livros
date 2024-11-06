from typing import List
from ninja import Query, Router
from .models import Categoria, Livro
from .schemas import AvaliacaoSchema, CategoriasViewSchema, FiltrosSortear, LivroSchema, LivrosViewSchema

categorias_router = Router()
livros_router = Router()

@categorias_router.get('/', response={200: List[CategoriasViewSchema]})
def get_categorias(request):
    categorias = Categoria.objects.all()
    return categorias

@livros_router.post('/', response={200: dict, 400:dict})
def create_livro(request, livro_schema: LivroSchema):

    nome = livro_schema.dict()['nome']
    streaming = livro_schema.dict()['streaming']
    categorias = livro_schema.dict()['categorias']
    
    # if not all([nome, streaming, categorias]):
    if not all([nome, streaming]):
        # return 400, {"status": "Nome, streaming e categorias devem ser informados."}
        return 400, {"status": "Nome e streaming deve ser informado."}

    livro = Livro(nome=nome, streaming=streaming)
    livro.save()

    livro.categorias.add(*categorias)
    livro.save()

    # return livro
    return 200, {"status": f"Livro cadastrado com sucesso."}

@livros_router.put('/{livro_id}', response={200:dict, 400:dict})
def avaliar_livro(request, livro_id: int, avaliacao_schema: AvaliacaoSchema):

    nota = avaliacao_schema.dict()['nota']
    comentario = avaliacao_schema.dict()['comentario']

    if not all([nota, comentario]):
        return 400, {'status': 'Informe a nota e o comentário.'}

    try:
        livro = Livro.objects.get(id=livro_id)

        livro.comentario = comentario
        livro.nota = nota
        livro.save()
        
        return 200, {'status': f'Avaliação realizada para o livro "{livro.nome}".'}
    
    except Livro.DoesNotExist:
        return {'status': 'Livro não cadastrado.'}
    except Exception as e:
        return {'status': f'Erro: {e}.'}

@livros_router.delete('/{livro_id}')
def deletar_livro(request, livro_id: int):
    try:
        livro = Livro.objects.get(id=livro_id)
        livro.delete()
    except Livro.DoesNotExist:
        return {'status': 'Livro não cadastrado.'}

    return 200, {'status': f'O Livro "{livro.nome}" foi excluído.'}

@livros_router.get('/sortear/', response={200: LivroSchema, 404: dict})
def sortear_livro(request, filtros: Query[FiltrosSortear]):
    nota_minima = filtros.dict()['nota_minima']
    categoria = filtros.dict()['categoria']
    lido = filtros.dict()['lido']

    livros = Livro.objects.all()

    if nota_minima:
        livros = livros.filter(nota__gte=nota_minima)

    if categoria:
        livros = livros.filter(categorias__id=categoria)

    if not lido:
        livros = livros.filter(nota=None)

    livro = livros.order_by('?').first()

    if livros.count() > 0:
        return livro
    else:
        return 404, {'status': 'Livro não sorteado'}

@livros_router.get('/', response={200: List[LivrosViewSchema]})
def get_livros(request):
    livros = Livro.objects.all()
    return livros
