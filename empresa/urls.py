from django.urls import path
from . import views

urlpatterns = [
    path('nova_empresa/', views.NovaEmpresa, name='nova_empresa'),
    path('empresas/', views.Empresas, name='empresas'),
    path('excluir_empresa/<int:id>', views.ExcluirEmpresa, name="excluir_empresa"),
]