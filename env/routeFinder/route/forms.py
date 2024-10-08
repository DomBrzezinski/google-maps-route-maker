from django import forms

class dataForm(forms.Form):
    # data = forms.CharField()
    starting_location = forms.CharField(label="Starting Location: ")
    return_original = forms.BooleanField(label="Return back here?")
    ending_location = forms.CharField(label="Ending Location: ")
    travel_method = forms.ChoiceField(widget=forms.RadioSelect, choices=[('1','Walking'),('2','Running'),('3','Bicycling')])
    time_or_distance = forms.ChoiceField(widget=forms.RadioSelect, choices=[('1','Time'),('2','Distance')])
    time_input = forms.IntegerField(label="Enter the time in minutes: ")
    distance_input = forms.FloatField(label="Enter the distance in kilometres: ")
    