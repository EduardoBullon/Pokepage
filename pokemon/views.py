import requests
from django.shortcuts import render, redirect, get_object_or_404
from .models import Pokemon, Equipo
from .forms import EquipoForm

import requests
from django.shortcuts import render, redirect, get_object_or_404
from .models import Pokemon, Equipo
from .forms import EquipoForm


def buscar_pokemon(request):
    if request.method == "GET" and 'nombre' in request.GET:
        nombre = request.GET['nombre'].lower()  # Obtener el nombre del Pokémon desde la solicitud GET
        url = f"https://pokeapi.co/api/v2/pokemon/{nombre}/"  # URL de la PokeAPI
        url_species = f"https://pokeapi.co/api/v2/pokemon-species/{nombre}/"  # URL para obtener la especie y descripción

        try:
            response = requests.get(url)  # Hacer la solicitud a la PokeAPI
            data = response.json()  # Convertir la respuesta a formato JSON

            # Obtener la descripción del Pokémon desde la especie
            response_species = requests.get(url_species)
            species_data = response_species.json()

            # Buscar la descripción (flavor_text_entries) en español
            description = None
            for entry in species_data['flavor_text_entries']:
                if entry['language']['name'] == 'es':  # Usamos el idioma español para la descripción
                    description = entry['flavor_text']
                    break

            # Extraer los atributos relevantes del Pokémon
            tipo = ', '.join([t['type']['name'] for t in data['types']])
            
            # Conversión de unidades
            altura = data['height'] / 10  # Convertir decímetros a metros
            peso = data['weight'] / 10  # Convertir hectogramos a kilogramos

            imagen = data['sprites']['front_default']  # Imagen
            numero_pokedex = data['id']  # Número en la Pokédex

            # Contexto a pasar a la plantilla
            context = {
                'pokemon': data['name'],
                'imagen': imagen,
                'altura': altura,  # Altura en metros
                'peso': peso,  # Peso en kilogramos
                'numero_pokedex': numero_pokedex,  # Añadimos el número de la Pokédex
                'tipos': tipo.split(', '),  # Convertir tipos en lista
                'descripcion': description  # Descripción en español del Pokémon
            }
            return render(request, 'pokemon/buscar_pokemon.html', context)

        except requests.exceptions.RequestException as e:
            return render(request, 'pokemon/buscar_pokemon.html', {'error': 'Pokémon no encontrado'})
    return render(request, 'pokemon/buscar_pokemon.html')


# Vista para crear un equipo de Pokémon
def crear_equipo(request):
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
    try:
        equipo = Equipo.objects.get(pk=pk)  # Obtiene el equipo por ID
        pokemon_equipo = equipo.pokemones.all()  # Accede a todos los Pokémon asociados a este equipo
        
        # No es necesario procesar los tipos de Pokémon aquí, lo gestionamos en la vista
        return render(request, 'pokemon/ver_equipo.html', {'equipo': equipo, 'pokemon_equipo': pokemon_equipo})
    except Equipo.DoesNotExist:
        return render(request, 'pokemon/ver_equipo.html', {'error': 'Equipo no encontrado'})

# Vista para editar un equipo existente
def editar_equipo(request, pk):
    equipo = get_object_or_404(Equipo, pk=pk)
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
    equipo = Equipo.objects.get(pk=pk)  # Obtener el equipo por su ID
    if request.method == 'POST':
        equipo.delete()  # Elimina el equipo
        return redirect('equipos')  # Redirige a la lista de equipos
    return render(request, 'pokemon/eliminar_equipo.html', {'equipo': equipo})
