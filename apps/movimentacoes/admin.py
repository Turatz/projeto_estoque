from django.contrib import admin
from .models import Movimentacao


@admin.register(Movimentacao)
class MovimentacaoAdmin(admin.ModelAdmin):
    list_display = ["criado_em", "produto", "tipo", "quantidade"]
    list_filter = ["tipo"]
    autocomplete_fields = ["produto"]
    list_select_related = ["produto"]

    def has_change_permission(self, request, obj=None):
        return obj is None

    def has_delete_permission(self, request, obj=None):
        return False