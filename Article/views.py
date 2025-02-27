from django.shortcuts import render, HttpResponse

# Create your views here.


def index(request):
    return HttpResponse("<h1 style='font-size: 500px;'>Hello</h1>")