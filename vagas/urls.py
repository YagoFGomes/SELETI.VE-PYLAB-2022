from django.urls import path
from . import views

urlpatterns = [
    path('nova_vaga/', views.NovaVaga, name="nova_vaga"),
    path('vaga/<int:id>', views.Vaga, name="vaga"),
    path('nova_tarefa/<int:id_vaga>', views.NovaTarefa, name='nova_tarefa'),
    path('realizar_tarefa/<int:id>', views.RealizarTarefa, name='realizar_tarefa'),
    path('envia_email/<int:id_vaga>', views.EnviaEmail, name="envia_email")
]