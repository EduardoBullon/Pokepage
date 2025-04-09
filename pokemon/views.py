from django.shortcuts import render, redirect, get_object_or_404
from .models import Pokemon, Equipo
from .forms import EquipoForm
import requests
from django.http import JsonResponse

# Vista para buscar un Pokémon
def buscar_pokemon(request):
    if request.method == "GET" and 'nombre' in request.GET:
        nombre = request.GET['nombre'].lower()
        url = f"https://pokeapi.co/api/v2/pokemon/{nombre}/"
        url_species = f"https://pokeapi.co/api/v2/pokemon-species/{nombre}/"

        try:
            response = requests.get(url)
            data = response.json()

            # Obtener la descripción
            response_species = requests.get(url_species)
            species_data = response_species.json()

            description = None
            for entry in species_data['flavor_text_entries']:
                if entry['language']['name'] == 'es': 
                    description = entry['flavor_text']
                    break

            tipo = ', '.join([t['type']['name'] for t in data['types']])
            altura = data['height'] / 10  # Convertir decímetros a metros
            peso = data['weight'] / 10  # Convertir hectogramos a kilogramos
            imagen = data['sprites']['front_default']
            numero_pokedex = data['id']

            context = {
                'pokemon': data['name'],
                'imagen': imagen,
                'altura': altura,
                'peso': peso,
                'numero_pokedex': numero_pokedex,
                'tipos': tipo.split(', '),
                'descripcion': description,
            }
            return render(request, 'pokemon/buscar_pokemon.html', context)

        except requests.exceptions.RequestException as e:
            return render(request, 'pokemon/buscar_pokemon.html', {'error': 'Pokémon no encontrado'})
    return render(request, 'pokemon/buscar_pokemon.html')


def crear_equipo(request):
    if request.method == "GET" and 'nombre' in request.GET:
        nombre = request.GET['nombre'].lower()  # Obtener el nombre del Pokémon desde la solicitud GET
        url = f"https://pokeapi.co/api/v2/pokemon/{nombre}/"  # URL de la PokeAPI

        try:
            response = requests.get(url)
            data = response.json()

            # Extraer la información relevante del Pokémon
            tipo = [t['type']['name'] for t in data['types']]  # Obtenemos los tipos como lista
            imagen_url = data['sprites']['front_default']
            numero_pokedex = data['id']
            altura = data['height'] / 10  # Convertir de decímetros a metros
            peso = data['weight'] / 10  # Convertir de hectogramos a kilogramos

            # Verificar si el Pokémon ya está en la base de datos
            pokemon, created = Pokemon.objects.get_or_create(
                nombre=data['name'],
                tipo=','.join(tipo),  # Guardar como cadena separada por comas
                altura=altura,
                peso=peso,
                imagen_url=imagen_url,
                numero_pokedex=numero_pokedex
            )

            context = {
                'pokemon': pokemon,
                'equipo_actual': Pokemon.objects.filter(id__in=request.session.get('equipo', []))  # Mostrar solo los Pokémon del equipo
            }

            return render(request, 'pokemon/crear_equipo.html', context)

        except requests.exceptions.RequestException as e:
            return render(request, 'pokemon/crear_equipo.html', {'error': 'Pokémon no encontrado'})

    return render(request, 'pokemon/crear_equipo.html')


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


from django.http import JsonResponse
from django.template.loader import render_to_string

# Añadir Pokémon al equipo al presionar el botón "Agregar al equipo"
# Añadir Pokémon al equipo al presionar el botón "Agregar al equipo"
# Vista para agregar Pokémon al equipo
def agregar_pokemon(request):
    if request.method == "POST":
        pokemon_id = request.POST.get('pokemon_id')
        if pokemon_id:
            # Verifica si la sesión del equipo ya existe, si no la crea
            if 'equipo' not in request.session:
                request.session['equipo'] = []

            # Asegúrate de que no haya más de 6 Pokémon en el equipo
            if len(request.session['equipo']) < 6:
                # Agregar el Pokémon si no está ya en el equipo
                if pokemon_id not in request.session['equipo']:
                    request.session['equipo'].append(pokemon_id)

                # Guardar la sesión
                request.session.modified = True

            # Obtener los Pokémon del equipo actual
            equipo_actual = Pokemon.objects.filter(id__in=request.session['equipo'])

            # Retornar el HTML actualizado para el equipo
            pokemon_seleccionados_html = render_to_string(
                'pokemon/seleccionados.html', {'equipo_actual': equipo_actual}
            )
            return JsonResponse({'pokemon_seleccionados_html': pokemon_seleccionados_html})
    
    return JsonResponse({'error': 'No se pudo agregar el Pokémon'}, status=400)
