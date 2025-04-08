import requests
from django.shortcuts import render, redirect
from .models import Pokemon, Equipo
from .forms import EquipoForm

# Vista para buscar un Pokémon desde la PokeAPI
def buscar_pokemon(request):
    if request.method == "GET" and 'nombre' in request.GET:
        nombre = request.GET['nombre'].lower()  # Obtener el nombre del Pokémon desde la solicitud GET
        url = f"https://pokeapi.co/api/v2/pokemon/{nombre}/"  # URL de la PokeAPI

        try:
            response = requests.get(url)  # Hacer la solicitud a la PokeAPI
            data = response.json()  # Convertir la respuesta a formato JSON

            # Extraer los tipos del Pokémon
            tipo = ', '.join([t['type']['name'] for t in data['types']])

            # Verificar si el Pokémon ya existe en la base de datos, si no, lo creamos
            pokemon, created = Pokemon.objects.get_or_create(
                nombre=data['name'],
                tipo=tipo
            )

            # Enviar el contexto con el Pokémon y su creación
            context = {
                'pokemon': pokemon,
                'created': created
            }
            return render(request, 'pokemon/buscar_pokemon.html', context)
        except requests.exceptions.RequestException as e:
            # Si ocurre un error en la solicitud
            return render(request, 'pokemon/buscar_pokemon.html', {'error': 'Pokémon no encontrado'})
    return render(request, 'pokemon/buscar_pokemon.html')


# Vista para crear un equipo de Pokémon
def crear_equipo(request):
    # Si el formulario se envía por POST
    if request.method == 'POST':
        form = EquipoForm(request.POST)
        if form.is_valid():  # Si el formulario es válido
            equipo = form.save()  # Guardamos el equipo en la base de datos
            return redirect('equipos')  # Redirigimos a la lista de equipos
    else:
        form = EquipoForm()

    # Si se recibe un nombre de Pokémon en GET, buscamos ese Pokémon
    if request.method == "GET" and 'nombre' in request.GET:
        nombre = request.GET['nombre'].lower()
        url = f"https://pokeapi.co/api/v2/pokemon/{nombre}/"

        try:
            response = requests.get(url)
            data = response.json()

            # Extraer la información relevante del Pokémon
            tipo = ', '.join([t['type']['name'] for t in data['types']])

            # Verificar si el Pokémon existe en la base de datos o crear uno nuevo
            pokemon, created = Pokemon.objects.get_or_create(
                nombre=data['name'],
                tipo=tipo
            )

            context = {
                'pokemon': pokemon,
                'created': created,
                'form': form
            }
            return render(request, 'pokemon/crear_equipo.html', context)
        
        except requests.exceptions.RequestException as e:
            return render(request, 'pokemon/crear_equipo.html', {'error': 'Pokémon no encontrado', 'form': form})

    return render(request, 'pokemon/crear_equipo.html', {'form': form})


# Vista para listar todos los equipos
def listar_equipos(request):
    equipos = Equipo.objects.all()  # Obtiene todos los equipos
    return render(request, 'pokemon/listar_equipos.html', {'equipos': equipos})


# Vista para ver los detalles de un equipo específico
def ver_equipo(request, pk):
    equipo = Equipo.objects.get(pk=pk)  # Obtiene el equipo por ID
    return render(request, 'pokemon/ver_equipo.html', {'equipo': equipo})


# Vista para editar un equipo existente
def editar_equipo(request, pk):
    equipo = Equipo.objects.get(pk=pk)
    if request.method == 'POST':
        form = EquipoForm(request.POST, instance=equipo)
        if form.is_valid():
            form.save()  # Guarda el equipo editado
            return redirect('ver_equipo', pk=equipo.pk)  # Redirige a la vista de detalles del equipo editado
    else:
        form = EquipoForm(instance=equipo)
    
    return render(request, 'pokemon/crear_equipo.html', {'form': form})


# Vista para eliminar un equipo
def eliminar_equipo(request, pk):
    equipo = Equipo.objects.get(pk=pk)
    if request.method == 'POST':
        equipo.delete()  # Elimina el equipo de la base de datos
        return redirect('equipos')  # Redirige a la lista de equipos

    return render(request, 'pokemon/eliminar_equipo.html', {'equipo': equipo})
