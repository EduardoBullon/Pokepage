# Generated by Django 5.2 on 2025-04-09 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon', '0005_alter_pokemon_nombre'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pokemon',
            name='nombre',
            field=models.CharField(max_length=100),
        ),
    ]
