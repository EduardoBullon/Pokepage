from django.urls import path
from . import views

urlpatterns = [
    path('buscar/', views.buscar_pokemon, name='buscar_pokemon'),  # La URL 'buscar/' está asociada a la vista 'buscar_pokemon'
    path('crear/', views.crear_equipo, name='crear_equipo'),  # Vista para crear equipos
    path('equipos/', views.listar_equipos, name='equipos'),  # Vista para listar equipos
    path('ver/<int:pk>/', views.ver_equipo, name='ver_equipo'),  # Vista para ver detalles del equipo
    path('editar/<int:pk>/', views.editar_equipo, name='editar_equipo'),  # Vista para editar un equipo
    path('eliminar/<int:pk>/', views.eliminar_equipo, name='eliminar_equipo'),  # Vista para eliminar un equipo
]
