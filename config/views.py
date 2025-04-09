# config/views.py
from django.shortcuts import render

# Vista para la página principal
def index(request):
    return render(request, 'index.html')  # Asegúrate de que el archivo index.html existe en la carpeta templates
