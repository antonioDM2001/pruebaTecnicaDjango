from rest_framework import serializers
from .models import Family, Animal, Zoo

class ZooSerializer(serializers.ModelSerializer):
    animal_names = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='scientific_name',
        source='animals'  
    )

    class Meta:
        model = Zoo
        fields = ['id', 'name', 'city', 'country', 'size_m2', 'annual_budget', 'animal_names']

