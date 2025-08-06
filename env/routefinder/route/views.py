from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from . import router
from .forms import dataForm
import os
from django.utils.datastructures import MultiValueDictKeyError

global form_data

def try_or_none(_form_data, context, context_name, form_name):
    try:
        context[context_name] = _form_data[form_name]
    except (MultiValueDictKeyError, KeyError):
        context[context_name] = ""
    return context


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
            form_data = form.data.copy()
            form_data["errors"] = form.errors.as_data()
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

    global form_data

    try: a = form_data
    except NameError: form_data = form.data
    

    context = {
        'form': form
    }

    if form_data != {}:

        if ro:
            context['return_original'] = True
     
        in_names = [['start_location', 'starting_location'],
                    ['end_location', 'ending_location'],
                    ['time_or_distance', 'time_or_distance'],
                    ['time', 'time_input'],
                    ['distance', 'distance_input'],
                    ['travel_method', 'travel_method'],
                    # ['return_original', 'return_original']
                    ]
        
        print(form_data)
        for in_name in in_names:
            context = try_or_none(form_data, context, in_name[0], in_name[1])

        print(form_data["errors"])
        errors = form_data["errors"]
        for field in errors:
            errors[field] = str(errors[field]).replace("[ValidationError(['", "").replace("'])]", "")

        context["form_errors"] = form_data["errors"]

    return HttpResponse(template.render(context, request))

