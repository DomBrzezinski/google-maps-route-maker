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
            print(input_data)
        else:
            pass #REDIRECT TO /INPUTS TO REFILL THE FORM PLEASSESEEE
    else:
        form = dataForm()

    with open(os.path.dirname(os.path.realpath(__file__)) + '\\key.txt', "r") as key_file:
        key_file.readline()
        website_key = key_file.readline()
    route_info = router.route_main(input_data)
    print(route_info)
    waypoints = route_info[1]
    waypoints.append(route_info[4])
    waypoints.insert(0, route_info[3])
    print(waypoints)
    travel_method = route_info[2].upper()
    context = {
        'website_key': website_key,
        'waypoints': waypoints,
        'travel_method': travel_method,
        'form': form,
        'start_location': input_data["starting_location"],
        'end_location': input_data["ending_location"],
        'return_original': input_data["return_original"],
        'time':  input_data["time_input"],
        'distance': input_data["distance_input"],
        'actual_distance': route_info[5],
        'actual_time': route_info[6]
    }
    form = dataForm()
    template = loader.get_template('index.html')
    return HttpResponse(template.render(context, request))


def inputs(request):
    form = dataForm()
    template = loader.get_template('no_map.html')
    context = {'form': form}
    return HttpResponse(template.render(context, request))
