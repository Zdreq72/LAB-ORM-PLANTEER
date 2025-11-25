from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from plants.models import Plant


def home_page(request):
    plants = Plant.objects.all()[:3]  
    return render(request, "home/home.html", {"plants": plants})
