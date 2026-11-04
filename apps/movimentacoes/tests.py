from django.core.exceptions import ValidationError
from django.test import TestCase

from apps.produtos.models import Categoria, Produto
from .models import Movimentacao


class MovimentacaoTests(TestCase):
    def setUp(self):
        cat = Categoria.objects.create(nome="Geral")
        self.produto = Produto.objects.create(nome="Caneta", sku="C1", categoria=cat)

    def test_entrada_aumenta_estoque(self):
        Movimentacao.objects.create(produto=self.produto, tipo="E", quantidade=10)
        self.produto.refresh_from_db()
        self.assertEqual(self.produto.quantidade_atual, 10)

    def test_saida_diminui_estoque(self):
        Movimentacao.objects.create(produto=self.produto, tipo="E", quantidade=10)
        Movimentacao.objects.create(produto=self.produto, tipo="S", quantidade=4)
        self.produto.refresh_from_db()
        self.assertEqual(self.produto.quantidade_atual, 6)

    def test_saida_maior_que_estoque_falha(self):
        with self.assertRaises(ValidationError):
            Movimentacao.objects.create(produto=self.produto, tipo="S", quantidade=1)