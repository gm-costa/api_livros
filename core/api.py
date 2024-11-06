from ninja import NinjaAPI
from livros.api import livros_router, categorias_router

api = NinjaAPI()

api.add_router('categorias/', categorias_router)
api.add_router('livros/', livros_router)
