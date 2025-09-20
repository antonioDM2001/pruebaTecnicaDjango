from rest_framework import serializers
from .models import Family, Animal, Zoo

class FamilySerializer(serializers.ModelSerializer):
    class Meta:
        model = Family
        fields = ('id', 'name')


class AnimalSpeciesSerializer(serializers.ModelSerializer):
    family = FamilySerializer(read_only=True)
    family_id = serializers.PrimaryKeyRelatedField(queryset=Family.objects.all(), source='family', write_only=True)


class Meta:
    model = Animal
    fields = ('id', 'common_name', 'scientific_name', 'family', 'family_id', 'endangered')

class ZooCreateSerializer(serializers.ModelSerializer):
    animals_scientific_names = serializers.ListField(
    child=serializers.CharField(), write_only=True, required=False,
    help_text='Lista de nombres científicos a asociar al zoo'
    )


    class Meta:
        model = Zoo
        fields = ('id', 'name', 'city', 'country', 'size_m2', 'annual_budget', 'animals_scientific_names')


    def _resolve_scientific_names(self, names):
        animals = AnimalSpecies.objects.filter(scientific_name__in=names)
        found = {a.scientific_name for a in animals}
        missing = set(names) - found
        return animals, missing


    def create(self, validated_data):
        names = validated_data.pop('animals_scientific_names', [])
        zoo = Zoo.objects.create(**validated_data)
        if names:
            animals, missing = self._resolve_scientific_names(names)
        if missing:
            raise serializers.ValidationError({'animals_scientific_names': f'No se encontraron especies: {", ".join(sorted(missing))}'})
        zoo.animals.set(animals)
        return zoo


    def update(self, instance, validated_data):
        names = validated_data.pop('animals_scientific_names', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if names is not None:
            animals, missing = self._resolve_scientific_names(names)
        if missing:
            raise serializers.ValidationError({'animals_scientific_names': f'No se encontraron especies: {", ".join(sorted(missing))}'})
        instance.animals.set(animals)
        return instance

class ZooListSerializer(serializers.ModelSerializer):
    animals_count = serializers.SerializerMethodField()
    animals_by_family = serializers.SerializerMethodField()


    class Meta:
        model = Zoo
        fields = ('id', 'name', 'city', 'country', 'size_m2', 'annual_budget', 'animals_count', 'animals_by_family')


    def get_animals_count(self, obj):
        return obj.animals.count()


    def get_animals_by_family(self, obj):
        # retorna un dict { 'Familia A': ['nombre vulgar 1', 'nombre vulgar 2'], ... }
        qs = obj.animals.select_related('family').all()
        grouped = {}
        for a in qs:
            fam = a.family.name
        grouped.setdefault(fam, []).append(a.common_name)
        return grouped

class ZooDetailSerializer(serializers.ModelSerializer):
    animals = AnimalSpeciesSerializer(many=True, read_only=True)
    animals_count = serializers.SerializerMethodField()
    animals_by_family = serializers.SerializerMethodField()


    class Meta:
        model = Zoo
        fields = ('id', 'name', 'city', 'country', 'size_m2', 'annual_budget', 'animals_count', 'animals_by_family', 'animals')


    def get_animals_count(self, obj):
        return obj.animals.count()


    def get_animals_by_family(self, obj):
        qs = obj.animals.select_related('family').all()
        grouped = {}
        for a in qs:
            fam = a.family.name
        grouped.setdefault(fam, []).append(a.common_name)
        return grouped