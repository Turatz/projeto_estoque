from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from .forms import CategoriaForm, ProdutoForm
from .models import Categoria, Produto
from django.db.models import Count
class FormMixin(LoginRequiredMixin):
    template_name = "form.html"
    titulo = ""
    msg_sucesso = "Salvo com sucesso."

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["titulo"] = self.titulo
        ctx["voltar"] = self.success_url
        return ctx

    def form_valid(self, form):
        messages.success(self.request, self.msg_sucesso)
        return super().form_valid(form)
class ApagarMixin(LoginRequiredMixin):
    template_name = "confirm_delete.html"
    msg_sucesso = "Apagado com sucesso."
    msg_erro = "Não é possível apagar: existem registros ligados a este item."

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["voltar"] = self.success_url
        return ctx

    def form_valid(self, form):
        try:
            response = super().form_valid(form)
        except ProtectedError:
            messages.error(self.request, self.msg_erro)
            return redirect(self.success_url)
        messages.success(self.request, self.msg_sucesso)
        return response
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
class ProdutoCreateView(FormMixin, CreateView):
    model = Produto
    form_class = ProdutoForm
    success_url = reverse_lazy("produtos:lista")
    titulo = "Novo produto"
    msg_sucesso = "Produto cadastrado."

    def get_initial(self):
        initial = super().get_initial()
        categoria = self.request.GET.get("categoria")
        if categoria:
            initial["categoria"] = categoria
        return initial
class ProdutoUpdateView(FormMixin, UpdateView):
    model = Produto
    form_class = ProdutoForm
    success_url = reverse_lazy("produtos:lista")
    titulo = "Editar produto"
    msg_sucesso = "Produto atualizado."
class ProdutoDeleteView(ApagarMixin, DeleteView):
    model = Produto
    success_url = reverse_lazy("produtos:lista")
    msg_sucesso = "Produto apagado."
    msg_erro = "Este produto tem movimentações e não pode ser apagado. Desative-o em Editar."
class CategoriaListView(LoginRequiredMixin, ListView):
    model = Categoria
    template_name = "produtos/categoria_list.html"
    context_object_name = "categorias"

    def get_queryset(self):
        return Categoria.objects.annotate(total=Count("produtos"))
class CategoriaDetailView(LoginRequiredMixin, DetailView):
    model = Categoria
    template_name = "produtos/categoria_detail.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["produtos"] = self.object.produtos.filter(ativo=True)
        return ctx
class CategoriaCreateView(FormMixin, CreateView):
    model = Categoria
    form_class = CategoriaForm
    success_url = reverse_lazy("produtos:categorias")
    titulo = "Nova categoria"
    msg_sucesso = "Categoria cadastrada."
class CategoriaUpdateView(FormMixin, UpdateView):
    model = Categoria
    form_class = CategoriaForm
    success_url = reverse_lazy("produtos:categorias")
    titulo = "Editar categoria"
    msg_sucesso = "Categoria atualizada."
class CategoriaDeleteView(ApagarMixin, DeleteView):
    model = Categoria
    success_url = reverse_lazy("produtos:categorias")
    msg_sucesso = "Categoria apagada."
    msg_erro = "Esta categoria tem produtos e não pode ser apagada."