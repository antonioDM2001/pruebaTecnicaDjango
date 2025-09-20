from django.shortcuts import render
from rest_framework import viewsets
from .models import Family, Animal, Zoo
from .serializers import FamilySerializer, AnimalSpeciesSerializer, ZooCreateSerializer, ZooListSerializer, ZooDetailSerializer

class FamilyViewSet(viewsets.ModelViewSet):
    queryset = Family.objects.all()
    serializer_class = FamilySerializer

class AnimalSpeciesViewSet(viewsets.ModelViewSet):
    queryset = Animal.objects.select_related('family').all()
    serializer_class = AnimalSpeciesSerializer


class ZooViewSet(viewsets.ModelViewSet):
    queryset = Zoo.objects.prefetch_related('animals__family').all()


def zoo_list_view(request):
    zoos = Zoo.objects.all().prefetch_related('animals')  # optimiza consultas
    return render(request, 'crudZoo/zoo_list.html', {'zoos': zoos})
    
def get_serializer_class(self):
    # Selección de serializer según la acción
    if self.action == 'list':
        return ZooListSerializer
    if self.action in ['create', 'update', 'partial_update']:
        return ZooCreateSerializer
    return ZooDetailSerializer
