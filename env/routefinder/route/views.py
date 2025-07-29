from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from . import router
from .forms import dataForm
import os
from django.utils.datastructures import MultiValueDictKeyError


def getRoute(request):

    if request.method == "POST":

        form = dataForm(request.POST)
        global ro
        try: 
            a = form.data["return_original"]
            ro = True
        except MultiValueDictKeyError: ro = False
        if form.is_valid():
            input_data = form.cleaned_data
            if ro: input_data["return_original"] = True
            print(input_data)
        else:
            global form_data
            form_data = form.data
            return HttpResponseRedirect('/inputs/')
               
    else:
        form = dataForm()

    if not (form.is_valid()):
        return HttpResponseRedirect('/inputs/')

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
    try:
        a = form_data['travel_method']
        # try: return_original = form_data['return_original']
        # except MultiValueDictKeyError: return_original = False
        context = {
            'form': form,
            'travel_method': form_data['travel_method'],
            'start_location': form_data["starting_location"],
            'end_location': form_data["ending_location"],
            'return_original': str(ro), 
            'time':  form_data["time_input"],
            'distance': form_data["distance_input"],
            'time_or_distance': form_data["time_or_distance"]
            }
        print(context)
    except NameError: 
        context = {'form': form}
    return HttpResponse(template.render(context, request))
