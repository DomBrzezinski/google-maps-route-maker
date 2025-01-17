from django import forms
import os
import googlemaps
from django.core.exceptions import ValidationError

class dataForm(forms.Form):
    # data = forms.CharField()
    starting_location = forms.CharField(label="Starting Location: ")
    return_original = forms.BooleanField(label="Return back here?", required=False)
    ending_location = forms.CharField(label="Ending Location: ", required=False)
    travel_method = forms.ChoiceField(widget=forms.RadioSelect, choices=[('Walking','Walking'),('Running','Running'),('Bicycling','Bicycling')])
    time_or_distance = forms.ChoiceField(widget=forms.RadioSelect, choices=[('1','Time'),('2','Distance')])
    time_input = forms.IntegerField(label="Enter the time in minutes: ", required=False)
    distance_input = forms.FloatField(label="Enter the distance in kilometres: ", required=False)
    # Creates the form fields


    def clean(self):
        cleaned_data = super().clean()
        start_loc = cleaned_data.get('starting_location')
        end_loc = cleaned_data.get('ending_location')
        return_o = cleaned_data.get('return_original')
        t_or_d = cleaned_data.get('time_or_distance')
        dist = cleaned_data.get('distance_input')
        time = cleaned_data.get('time_input')
        travel_method = cleaned_data.get('travel_method')
        # Retrieves the data from the form


        with open(os.path.dirname(os.path.realpath(__file__)) + '\\key.txt', "r") as key_file:
            directions_key = key_file.readline()

        gmaps = googlemaps.Client(key=directions_key)

        if gmaps.geocode(start_loc) == []:
            raise ValidationError("Invalid starting location")
        # Checks if the starting location is valid

        print(return_o, start_loc, end_loc)
        if not return_o:

            

            if not end_loc:
                raise ValidationError("Please enter an ending location")

            if gmaps.geocode(end_loc) == []:
                raise ValidationError("Invalid ending location")
            # Checks if the ending location is valid


            directions = gmaps.directions(start_loc, end_loc, mode=travel_method.lower())

            route_distance = 0 
            for leg in directions[0]["legs"]: 
                leg_distance = leg["distance"]["text"]
                if "km" in leg_distance:
                    leg_distance = float(leg_distance[:-2].replace(",",""))*1000
                else:
                    leg_distance = float(leg_distance[:-1].replace(",",""))*1000
                route_distance += leg_distance
            route_distance = int(route_distance)
            ### Calculates the distance of the returned route

            route_time = 0 
            for leg in directions[0]["legs"]: 
                leg_time = leg["duration"]["text"]
                leg_time = int(leg_time[:-4])
                route_time += leg_time
            route_time = int(route_time)
            ### Calculates the time of the returned route

            if t_or_d.lower() == "time":
                if not time:
                    raise ValidationError("Please enter a time")
                if route_time > time:
                    raise ValidationError("The route will take longer than the time you have specified")
            # Checks if the route time is longer than the time specified by the user
                
            elif t_or_d.lower() == "distance":
                if not dist:
                    raise ValidationError("Please enter a distance")
                if route_distance > dist:
                    raise ValidationError("The route is longer than the distance you have specified")
            # Checks if the route distance is longer than the distance specified by the user