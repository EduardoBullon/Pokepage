# Generated by Django 5.2 on 2025-04-09 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon', '0004_alter_pokemon_numero_pokedex'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pokemon',
            name='nombre',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
