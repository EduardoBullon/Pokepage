from django.shortcuts import render

def index(request):
    return render(request, 'index.html')  # Renderiza la plantilla index.html
