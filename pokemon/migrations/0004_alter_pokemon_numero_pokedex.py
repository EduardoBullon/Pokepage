# Generated by Django 5.2 on 2025-04-09 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon', '0003_pokemon_numero_pokedex'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pokemon',
            name='numero_pokedex',
            field=models.IntegerField(),
        ),
    ]
