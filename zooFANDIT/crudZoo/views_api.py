from rest_framework import viewsets,status
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, redirect,render
from .forms import ZooForm 
from .models import Zoo,Animal
from .serializers import ZooSerializer

class ZooViewSet(viewsets.ViewSet):
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer]

    def list(self, request):
        zoos = Zoo.objects.all()
        serializer = ZooSerializer(zoos, many=True)

        zoo_data = []
        for zoo in zoos:
            animals_by_family = {}
            for animal in zoo.animals.all():
                family_name = animal.family.name if animal.family else "Sin familia"
                animals_by_family.setdefault(family_name, []).append(animal.common_name)

            zoo_data.append({
                "zoo": zoo,
                "animal_count": zoo.animals.count(),
                "animals_by_family": animals_by_family
            })

        if request.accepted_renderer.format == "html":
            return Response({"zoo_data": zoo_data}, template_name="crudZoo/zoo_list.html")

        return Response(serializer.data)

    def create(self, request):
        if request.accepted_renderer.format == "html":
            if request.method == "POST":
                form = ZooForm(request.POST)
                if form.is_valid():
                    form.save()
                    return redirect("zoo-list")
            else:
                form = ZooForm()
            return Response({"form": form, "title": "Crear Nuevo Zoo"}, template_name="crudZoo/zoo_form.html")

        serializer = ZooSerializer(data=request.data)
        if serializer.is_valid():
            zoo = serializer.save()
            return Response(ZooSerializer(zoo).data)
        return Response(serializer.errors, status=400)


    def edit(self, request, pk=None):
        zoo = get_object_or_404(Zoo, pk=pk)

        if request.method == "GET":
            form = ZooForm(instance=zoo)
            return Response({"form": form, "title": f"Editar Zoo: {zoo.name}"}, template_name="crudZoo/zoo_form.html")

        if request.content_type == "application/json":
            serializer = ZooSerializer(zoo, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=400)
        else:
            form = ZooForm(request.POST, instance=zoo)
            if form.is_valid():
                form.save()
                return redirect("zoo-list")
            return Response({"form": form, "title": f"Editar Zoo: {zoo.name}"}, template_name="crudZoo/zoo_form.html", status=400)


    def delete(self, request, pk=None):
        zoo = get_object_or_404(Zoo, pk=pk)

        if request.method == "POST" or request.accepted_renderer.format == "json":
            zoo.delete()
            if request.accepted_renderer.format == "html":
                return redirect("zoo-list")
            return Response({"detail": "Zoo eliminado"}, status=status.HTTP_204_NO_CONTENT)

        return Response({"zoo": zoo}, template_name="crudZoo/zoo_confirm_delete.html")

