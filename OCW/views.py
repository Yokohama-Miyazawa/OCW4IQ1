from django.shortcuts import render
from django.core import serializers
# from . models import feed
import json
# Create your views here.


def index(request):
    template = 'OCW/index.html'
    # results = feed.objects.all()
    results = "これは仮文字列です．IQ1"
    context = {
        'results': results,
    }
    return render(request, template, context)


def getdata(request):
    # results = feed.objects.all()
    results = "これは仮文字列です．IQ1"
    jsondata = serializers.serialize('json', results)
    return HttpResponse(jsondata)


def base_layout(request):
    template = 'OCW/base.html'
    return render(request, template)
