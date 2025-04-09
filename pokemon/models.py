from django.db import models

class Pokemon(models.Model):
    nombre = models.CharField(max_length=100)  # Asegura que no haya Pokémon con el mismo nombre
    tipo = models.CharField(max_length=100, default="Desconocido")  # Valor por defecto para tipo
    altura = models.FloatField(default=0.0)  # Valor por defecto para altura
    peso = models.FloatField(default=0.0)  # Valor por defecto para peso
    imagen_url = models.URLField(default="https://example.com/default-image.png")  # Usamos URL para imagen
    numero_pokedex = models.IntegerField()  # Guardamos el número de la Pokédex

    def __str__(self):
        return self.nombre

class Equipo(models.Model):
    nombre = models.CharField(max_length=100)
    pokemones = models.ManyToManyField(Pokemon, related_name='equipos')  # Relación muchos a muchos

    def __str__(self):
        return self.nombre
