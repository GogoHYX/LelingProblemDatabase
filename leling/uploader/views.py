from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader

from .models import *


def index(request):
    template = loader.get_template('uploader/index.html')
    context = {
        'type_list': Question.TYPE_SLUGS, }
    return HttpResponse(template.render(context, request))


def add(request):
    pass


def multiple_choice(request):
    template = loader.get_template('uploader/MC.html')
    return HttpResponse(template.render(request))
