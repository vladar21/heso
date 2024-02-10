from django.shortcuts import render
from django.http import HttpResponse


def my_schedule(request):
    return HttpResponse("Hello, Schedule!")
