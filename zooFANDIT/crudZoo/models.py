from django.db import models

class Family(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = 'Familia'
        verbose_name_plural = 'Familias'


def __str__(self):
    return self.name

class Animal(models.Model):
    common_name = models.CharField('Nombre vulgar', max_length=200)
    scientific_name = models.CharField('Nombre científico', max_length=200, unique=True)
    family = models.ForeignKey(Family, related_name='species', on_delete=models.PROTECT)
    endangered = models.BooleanField('En peligro de extinción', default=False)


    class Meta:
        verbose_name = 'Especie'
        verbose_name_plural = 'Especies'


def __str__(self):
    return f"{self.common_name} ({self.scientific_name})"

class Zoo(models.Model):
    name = models.CharField('Nombre', max_length=255)
    city = models.CharField('Ciudad', max_length=100)
    country = models.CharField('País', max_length=100)
    size_m2 = models.PositiveIntegerField('Tamaño (m2)')
    annual_budget = models.DecimalField('Presupuesto anual', max_digits=14, decimal_places=2)
    animals = models.ManyToManyField(Animal, related_name='zoos', blank=True)


    class Meta:
        verbose_name = 'Zoo'
        verbose_name_plural = 'Zoos'


def __str__(self):
    return self.name
