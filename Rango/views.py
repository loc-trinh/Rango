from django.shortcuts import render
from django.http import HttpResponse


def index(requests):
    context = {'boldmessage': "Welcome to RANGO"}
    return render(requests, "Rango/index.html", context)


def about(requests):
    html = "<p>This is the about page</p><a href='/rango'>Index</a>"
    return HttpResponse(html)
