from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.db.models import F, Q

from apps.produtos.models import Produto


class Movimentacao(models.Model):
    ENTRADA = "E"
    SAIDA = "S"
    TIPOS = [(ENTRADA, "Entrada"), (SAIDA, "Saída")]

    produto = models.ForeignKey(Produto, on_delete=models.PROTECT, related_name="movimentacoes")
    tipo = models.CharField(max_length=1, choices=TIPOS)
    quantidade = models.PositiveIntegerField()
    observacao = models.CharField(max_length=255, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-criado_em"]
        constraints = [
            models.CheckConstraint(
                condition=Q(quantidade__gt=0), name="movimentacao_qtd_positiva"
            ),
        ]

    def __str__(self):
        return f"{self.get_tipo_display()} de {self.quantidade} - {self.produto}"

    def save(self, *args, **kwargs):
        if self.pk:
            raise ValidationError("Movimentações não podem ser editadas.")
        with transaction.atomic():
            produto = Produto.objects.select_for_update().get(pk=self.produto_id)
            if self.tipo == self.SAIDA and self.quantidade > produto.quantidade_atual:
                raise ValidationError("Estoque insuficiente para esta saída.")
            super().save(*args, **kwargs)
            delta = self.quantidade if self.tipo == self.ENTRADA else -self.quantidade
            Produto.objects.filter(pk=produto.pk).update(
                quantidade_atual=F("quantidade_atual") + delta
            )