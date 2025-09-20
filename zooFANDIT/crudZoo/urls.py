#from rest_framework.routers import DefaultRouter
from .views import FamilyViewSet, AnimalSpeciesViewSet, ZooViewSet
from django.urls import path
from .views import zoo_list_view, zoo_create_view


#router = DefaultRouter()
#router.register(r'families', FamilyViewSet, basename='family') #A implementar la view
#router.register(r'animals', AnimalSpeciesViewSet, basename='animal') #A implementar la view
#router.register(r'zoos', ZooViewSet, basename='zoo')#A implementar la view


#urlpatterns = router.urls
urlpatterns = [
    path('', zoo_list_view, name='zoo-list'),
    path('create/',zoo_create_view, name='zoo-create'),
]