from django.db import models


class Categoria(models.Model):
    nome = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ["nome"]

    def __str__(self):
        return self.nome


class Produto(models.Model):
    nome = models.CharField(max_length=150)
    sku = models.CharField("Código (SKU)", max_length=50, unique=True)
    categoria = models.ForeignKey(
        Categoria, on_delete=models.PROTECT, related_name="produtos"
    )
    preco_custo = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    preco_venda = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    quantidade_atual = models.IntegerField(default=0, editable=False)
    estoque_minimo = models.PositiveIntegerField(default=0)
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["nome"]
        indexes = [models.Index(fields=["nome"])]

    def __str__(self):
        return f"{self.sku} - {self.nome}"

    @property
    def abaixo_do_minimo(self):
        return self.quantidade_atual <= self.estoque_minimo