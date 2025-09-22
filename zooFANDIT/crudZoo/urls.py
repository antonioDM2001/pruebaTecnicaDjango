#from rest_framework.routers import DefaultRouter
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("crudZoo.urls_api")),
]