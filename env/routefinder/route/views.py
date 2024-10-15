from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from . import router
from .forms import dataForm
import os

def getRoute(request):

    if request.method == "POST":
        form = dataForm(request.POST)
        if form.is_valid():
            input_data = form.cleaned_data
    else:
        form = dataForm()

    
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
        'travel_method': travel_method,
        'form': form
    }
    template = loader.get_template('index.html')
    return HttpResponse(template.render(context, request))


def inputs(request):
    form = dataForm()
    template = loader.get_template('no_map.html')
    context = {'form': form}
    return HttpResponse(template.render(context, request))
