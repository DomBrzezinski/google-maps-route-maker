from django import forms
import os
import googlemaps
from django.core.exceptions import ValidationError

class dataForm(forms.Form):
    # data = forms.CharField()
    starting_location = forms.CharField(label="Starting Location: ", required=False)
    return_original = forms.BooleanField(label="Return back here?", required=False)
    ending_location = forms.CharField(label="Ending Location: ", required=False)
    travel_method = forms.ChoiceField(widget=forms.RadioSelect, choices=[('Walking','Walking'),('Running','Running'),('Bicycling','Bicycling')], required=False)
    time_or_distance = forms.ChoiceField(widget=forms.RadioSelect, choices=[('1','Time'),('2','Distance')], required=False)
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

        if travel_method == "":
            self.add_error('travel_method', "Please select a travel method")
            # raise ValidationError("Please select a travel method")


        with open(os.path.dirname(os.path.realpath(__file__)) + '\\key.txt', "r") as key_file:
            directions_key = key_file.readline()

        gmaps = googlemaps.Client(key=directions_key)

        if not start_loc:
            self.add_error('starting_location', "Please enter a starting location")
            # raise ValidationError("Please enter a starting location")
        else:
            if gmaps.geocode(start_loc) == []:
                self.add_error('starting_location', "Invalid starting location")
                # raise ValidationError("Invalid starting location")
            # Checks if the starting location is valid

        print(return_o, start_loc, end_loc)
        if not return_o:

            

            if not end_loc:
                self.add_error('ending_location', "Please enter an ending location")
                self._errors
                # raise ValidationError("Please enter an ending location")

            else:
                if gmaps.geocode(end_loc) == []:
                    self.add_error('ending_location', "Invalid ending location")
                    # raise ValidationError("Invalid ending location")
                # Checks if the ending location is valid

            if start_loc and end_loc:
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

                if t_or_d == None: t_or_d = "2"

                if t_or_d == "1":
                    if not time:
                        self.add_error('time_input', "Please enter a time")
                        # raise ValidationError("Please enter a time")
                    elif route_time > time:
                        self.add_error('time_input', "The route will take longer than the time you have specified")
                        # raise ValidationError("The route will take longer than the time you have specified")
                # Checks if the route time is longer than the time specified by the user
                    
                elif t_or_d == "2":
                    print(route_distance, dist, "rd")
                    if not dist:
                        self.add_error('distance_input', "Please enter a distance")
                        # raise ValidationError("Please enter a distance")                   
                    elif route_distance > dist*1000:
                        self.add_error('distance_input', "The route is longer than the distance you have specified")
                        # raise ValidationError("The route is longer than the distance you have specified")
                else:
                    self.add_error('time_or_distance', "Please select either time or distance")
                    # raise ValidationError("Please select either time or distance")

                # Checks if the route distance is longer than the distance specified by the user
            else:
                if t_or_d == None:
                    t_or_d = "2"
                if t_or_d == "1":
                    if not time:
                        self.add_error('time_input', "Please enter a time")
                elif t_or_d == "2":
                    if not dist:
                        self.add_error('distance_input', "Please enter a distance")
                else:
                    self.add_error('time_or_distance', "Please select either time or distance")
