from django.contrib import admin
from .models import Categoria, Livro


class LivroAdmin(admin.ModelAdmin):
    model = Livro
    list_display = ['nome', 'streaming', 'nota', 'id']

admin.site.register(Categoria)
admin.site.register(Livro, LivroAdmin)
