from django.shortcuts import render
# from django.http import HttpResponse
from .models import EnglishClass


def home(request):
    classes = EnglishClass.objects.all()  # Getting all english classes
    return render(request, 'scheduling/home.html', {'classes': classes})
