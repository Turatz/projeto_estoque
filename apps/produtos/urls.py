from django.urls import path
from . import views

app_name = "produtos"

urlpatterns = [

    path("", views.ProdutoListView.as_view(), name="lista"),
    path("novo/", views.ProdutoCreateView.as_view(), name="novo"),
    path("<int:pk>/editar/", views.ProdutoUpdateView.as_view(), name="editar"),
    path("<int:pk>/apagar/", views.ProdutoDeleteView.as_view(), name="apagar"),
    path("categorias/", views.CategoriaListView.as_view(), name="categorias"),
    path("categorias/nova/", views.CategoriaCreateView.as_view(), name="categoria_nova"),
    path("categorias/<int:pk>/", views.CategoriaDetailView.as_view(), name="categoria_detalhe"),
    path("categorias/<int:pk>/editar/", views.CategoriaUpdateView.as_view(), name="categoria_editar"),
    path("categorias/<int:pk>/apagar/", views.CategoriaDeleteView.as_view(), name="categoria_apagar"),
]