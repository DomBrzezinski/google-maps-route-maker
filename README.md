This is a project in progress, feel free to download and use it yourself, or modify it to your needs.
All work here is freely available to anyone.

This program creates a walking, running or cycling route in your area.
It uses googlemaps library in python: (https://github.com/googlemaps/google-maps-services-python).
It currently only displays the waypoints as a string on the webpage, but I am working on passing this data into an embedded Google Map.

INSTRUCTIONS:
Download files and create a .txt file named "key.txt" in the same env/routefinder/route directory. In the file, paste your Google API Key for Geocoding, Directions, Geolocation, Places and Roads APIs on line one and paste the Google API key for Directions, Maps Embed, Maps JavaScript and Maps Static APIs on line two and and save the file. You can get a Google Cloud Platform account and Google API Key at "https://console.cloud.google.com/".

Run the Django server and go to 127.0.0.1:8000/route/
Enter information in the command line as it asks for it. Currently working on displaying the map on the webpage
