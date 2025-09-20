from django import forms
from .models import Zoo, Animal

class ZooForm(forms.ModelForm):
    animals = forms.ModelMultipleChoiceField(
        queryset=Animal.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Zoo
        fields = ['name', 'city', 'country', 'size_m2', 'annual_budget', 'animals']