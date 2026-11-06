from django import forms
from .models import Categoria, Produto

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ["nome"]

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = [
            "nome", "sku", "categoria",
            "preco_custo", "preco_venda",
            "estoque_minimo", "ativo",
        ]
        