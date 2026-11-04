from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from .models import Produto


class ProdutoListView(LoginRequiredMixin, ListView):
    model = Produto
    template_name = "produtos/produto_list.html"
    context_object_name = "produtos"
    paginate_by = 20

    def get_queryset(self):
        qs = Produto.objects.select_related("categoria").filter(ativo=True)
        busca = self.request.GET.get("q")
        if busca:
            qs = qs.filter(nome__icontains=busca)
        return qs