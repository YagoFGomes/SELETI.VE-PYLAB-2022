from django.urls import path
from . import views

urlpatterns = [
    path('nova_vaga/', views.NovaVaga, name="nova_vaga")
]