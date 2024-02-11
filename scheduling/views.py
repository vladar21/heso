from django.shortcuts import render
# from django.http import HttpResponse
from .models import EnglishClass


def schedule(request):
    classes = EnglishClass.objects.all()  # Getting all english classes
    return render(request, 'scheduling/schedule.html', {'classes': classes})
