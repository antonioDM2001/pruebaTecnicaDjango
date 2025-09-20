"""
URL configuration for zooFANDIT project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.http import JsonResponse

def root_view(request):
    return JsonResponse({
        "message": "Bienvenido a la API de Fandit Zoo 🦁",
        "endpoints": {
            "admin": "/admin/",
            "api_zoos": "/api/zoos/",
            "api_animals": "/api/animals/",
            "api_families": "/api/families/",
        }
    })
    
urlpatterns = [
    path('admin/', admin.site.urls),
    #path("", root_view),
    path('', include('crudZoo.urls')),
    #path('api/', include('crudZoo.urls')),
]
