from django.shortcuts import render,redirect,get_object_or_404
from rest_framework import viewsets
from .models import Family, Animal, Zoo
from .forms import ZooForm
from .serializers import FamilySerializer, AnimalSpeciesSerializer, ZooCreateSerializer, ZooListSerializer, ZooDetailSerializer
from collections import defaultdict
from django.http import JsonResponse


def zoo_list_view(request):
    zoos = Zoo.objects.all().prefetch_related('animals__family')

    zoo_data = []
    for zoo in zoos:
        animals = zoo.animals.all()
        count = animals.count()

        grouped = defaultdict(list)
        for animal in animals:
            grouped[animal.family.name].append(animal.common_name)

        zoo_data.append({
            "zoo": zoo,
            "animal_count": count,
            "animals_by_family": dict(grouped),
        })

    return render(request, 'crudZoo/zoo_list.html', {'zoo_data': zoo_data})

def zoo_create_view(request):
    if request.method == 'POST':
        form = ZooForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('zoo-list')
    else:
        form = ZooForm()
    return render(request, 'crudZoo/zoo_form.html', {'form': form, 'title': 'Crear Zoo'})   


def zoo_delete_view(request, pk):
    zoo = get_object_or_404(Zoo, pk=pk)

    if request.method == "POST":
        zoo.delete()
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': True})
        return redirect('zoo-list')

    return redirect('zoo-list')
    
def zoo_update_view(request, pk):
    zoo = get_object_or_404(Zoo, pk=pk)
    if request.method == 'POST':
        form = ZooForm(request.POST, instance=zoo)
        if form.is_valid():
            form.save()
            return redirect('zoo-list')
    else:
        form = ZooForm(instance=zoo)
    return render(request, 'crudZoo/zoo_form.html', {'form': form, 'title': f'Editar {zoo.name}'})
    