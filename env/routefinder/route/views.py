from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from . import router
import os

def getRoute(request):
    template = loader.get_template('index.html')
    with open(os.path.dirname(os.path.realpath(__file__)) + '\\key.txt', "r") as key_file:
        key_file.readline()
        website_key = key_file.readline()
    waypoints = router.route_main()[1]
    context = {
        'website_key': website_key,
        'waypoints': waypoints
    }
    return HttpResponse(template.render(context, request))
