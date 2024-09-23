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
    route_info = router.route_main()
    print(route_info)
    print(route_info[2])
    waypoints = route_info[1]
    travel_method = route_info[2].upper()
    context = {
        'website_key': website_key,
        'waypoints': waypoints,
        'travel_method': travel_method
    }
    return HttpResponse(template.render(context, request))


def inputs(request):
    template = loader.get_template('no_map.html')
    context = {}
    return HttpResponse(template.render(context, request))
