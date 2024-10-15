from django import forms

class dataForm(forms.Form):
    # data = forms.CharField()
    starting_location = forms.CharField(label="Starting Location: ")
    return_original = forms.BooleanField(label="Return back here?", required=False)
    ending_location = forms.CharField(label="Ending Location: ", required=False)
    travel_method = forms.ChoiceField(widget=forms.RadioSelect, choices=[('Walking','Walking'),('Running','Running'),('Bicycling','Bicycling')])
    time_or_distance = forms.ChoiceField(widget=forms.RadioSelect, choices=[('1','Time'),('2','Distance')])
    time_input = forms.IntegerField(label="Enter the time in minutes: ", required=False)
    distance_input = forms.FloatField(label="Enter the distance in kilometres: ", required=False)
