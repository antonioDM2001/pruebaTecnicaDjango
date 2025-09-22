from django.urls import path
from .views_api import ZooViewSet

zoo_list = ZooViewSet.as_view({"get": "list"})
zoo_create = ZooViewSet.as_view({"get": "create", "post": "create"})
zoo_edit = ZooViewSet.as_view({"get": "edit", "post": "edit"})
zoo_delete = ZooViewSet.as_view({"post": "delete"})

urlpatterns = [
    path("", zoo_list, name="zoo-list"), 
    path("create/", zoo_create, name="zoo-create"),
    path("<int:pk>/edit/", zoo_edit, name="zoo-edit"),
    path("<int:pk>/delete/", zoo_delete, name="zoo-delete"),
]
