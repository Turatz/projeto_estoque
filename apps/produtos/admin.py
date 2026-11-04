from django.contrib import admin
from .models import Categoria, Produto


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    search_fields = ["nome"]


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ["sku", "nome", "categoria", "quantidade_atual", "estoque_minimo", "ativo"]
    list_filter = ["categoria", "ativo"]
    search_fields = ["nome", "sku"]
    list_select_related = ["categoria"]