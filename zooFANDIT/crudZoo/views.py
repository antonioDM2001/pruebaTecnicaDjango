from django.shortcuts import render,redirect
from rest_framework import viewsets
from .models import Family, Animal, Zoo
from .forms import ZooForm
from .serializers import FamilySerializer, AnimalSpeciesSerializer, ZooCreateSerializer, ZooListSerializer, ZooDetailSerializer
from collections import defaultdict

class FamilyViewSet(viewsets.ModelViewSet):
    queryset = Family.objects.all()
    serializer_class = FamilySerializer

class AnimalSpeciesViewSet(viewsets.ModelViewSet):
    queryset = Animal.objects.select_related('family').all()
    serializer_class = AnimalSpeciesSerializer


class ZooViewSet(viewsets.ModelViewSet):
    queryset = Zoo.objects.prefetch_related('animals__family').all()


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
    
def get_serializer_class(self):
    # Selección de serializer según la acción
    if self.action == 'list':
        return ZooListSerializer
    if self.action in ['create', 'update', 'partial_update']:
        return ZooCreateSerializer
    return ZooDetailSerializer
