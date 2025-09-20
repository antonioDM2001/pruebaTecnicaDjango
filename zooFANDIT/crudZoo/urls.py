from rest_framework.routers import DefaultRouter
from .views import FamilyViewSet, AnimalSpeciesViewSet, ZooViewSet


router = DefaultRouter()
router.register(r'families', FamilyViewSet, basename='family') #A implementar la view
router.register(r'animals', AnimalSpeciesViewSet, basename='animal') #A implementar la view
router.register(r'zoos', ZooViewSet, basename='zoo')#A implementar la view


urlpatterns = router.urls