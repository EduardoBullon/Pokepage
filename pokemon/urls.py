# pokemon/urls.py
from django.urls import path
from . import views  # Importa las vistas desde pokemon/views.py

urlpatterns = [
    path('buscar/', views.buscar_pokemon, name='buscar_pokemon'),
    path('crear/', views.crear_equipo, name='crear_equipo'),
    path('equipos/', views.listar_equipos, name='equipos'),
    path('equipo/<int:pk>/', views.ver_equipo, name='ver_equipo'),
    path('equipo/<int:pk>/eliminar/', views.eliminar_equipo, name='eliminar_equipo'),
    # Agrega la ruta para editar un equipo
    path('equipo/<int:pk>/editar/', views.editar_equipo, name='editar_equipo'),
]
