from django.shortcuts import render

from django.http import HttpResponse
from django.template import loader

def index(request):
    template = loader.get_template('polls/index.html')
    context = { 'name': 'Javier'}
    return render(request, 'polls/index.html', context)

def generic(request):
    template = loader.get_template('polls/generic.html')
    context = { 'name': 'Javier'}
    return render(request, 'polls/generic.html', context)

def results(request, number):
    response = "You chose number %s."
    return HttpResponse(response % number)

# Create your views here.
