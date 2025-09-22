from django.contrib import admin
from .models import Family, Animal, Zoo


@admin.register(Family)
class FamilyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Animal)
class AnimalSpeciesAdmin(admin.ModelAdmin):
    list_display = ('id', 'common_name', 'scientific_name', 'family', 'endangered')
    list_filter = ('family', 'endangered')
    search_fields = ('common_name', 'scientific_name')


@admin.register(Zoo)
class ZooAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'city', 'country', 'size_m2', 'annual_budget')
    search_fields = ('name', 'city', 'country')
    filter_horizontal = ('animals',)
