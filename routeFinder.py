### This program generates a running, cycling or walking route from a distance or length of time given by the user
### 1 degree of latitude is the 111,139 meters
import googlemaps
import datetime
import math as maths
from pprint import pprint



API_KEY = "AIzaSyDCNGvyU0JPwZqoCq-ZyMlCx1YQsnqJG9Y"
gmaps = googlemaps.Client(key=API_KEY)
### Receives the Google Maps Client to send requests to


def generate_semicircle(start_circumference,end_circumference):
    """
    generates a semicicle or semi-ellipse of given radius at the start coordinates
    INPUT: both vertices of the semicircle, or semi-ellipse
    OUTPUT: waypoints(global variable)
    """
    if start_coordinates == end_coordinates:
        waypoints[0] = [start_coordinates[0] - radius, start_coordinates[1]]
        waypoints[1] = [start_coordinates[0] - (maths.sin(45)*radius),
                        start_coordinates[1] + (maths.sin(45)*radius),]
        waypoints[2] = [start_coordinates[0], start_coordinates[1] + radius]
        waypoints[3] = [start_coordinates[0] + (maths.sin(45)*radius),
                        start_coordinates[1] + (maths.sin(45)*radius),]
        waypoints[4] = [start_coordinates[0] + radius, start_coordinates[1]]
        ### Changes all of the waypoints to be in a semicircle of given distance
    else:
        direct_gradient = (end_coordinates[1] - start_coordinates[1])/(end_coordinates[0] - start_coordinates[0])
        direct_distance = maths.sqrt(((end_coordinates[0] - start_coordinates[0])**2)+((end_coordinates[1] - start_coordinates[1])**2))
        print("INCOMPLETE")
        




def generate_route(**kwargs):
    """ 
    generates a route in the local area 
    INPUT: 
            start_location -- The starting address in formatted address form
            end_location -- The ending address in formatted address form
            distance -- The distance given for the route(optional)
            time -- The time given for the route(optional)
            travel_method -- The travel method for the route
            locationlonger -- If the route needs to be longer(boolean)
    OUTPUT: 
            Calculated route to be checked for user requirements outside of the function
    """

    global radius
    if start_coordinates == end_coordinates:
        if times_changed == 0:
            print(kwargs)
            if kwargs["distance"] != "":
                radius = kwargs["distance"]/(maths.pi + 2.0)
            ### Finds the optimum radius of a semicircle route for the distance given


            else:
                if kwargs["travel_method"] == "running":
                    radius = 250*kwargs["time"]/(maths.pi + 2.0) 
                elif kwargs["travel_method"] == "bicycling":
                    radius = 500*kwargs["time"]/(maths.pi + 2.0)
                elif kwargs["travel_method"] == "walking":
                    radius = 100*kwargs["time"]/(maths.pi + 2.0)
            ### Estimates distance travelled in time given based on mode of transport, making a semicircle radius


            radius = radius/111139 
            ### Converts to degrees


        else:  ### If this is not the first call of the function, ie it has to be changed from original radius
            if kwargs["longer"]:
                radius *= 1.2
            else:
                radius /= 1.3
        print(radius,times_changed,kwargs["longer"])
        start_semicircle = [start_coordinates[0] - radius,start_coordinates[1]]
        end_semicircle = [start_coordinates[0] + radius, start_coordinates[1]]
        generate_semicircle(start_semicircle,end_semicircle)
    ### Makes a semicircular route with adjusted radius based on the "longer" key
    

    else:
        # I WILL CHANGE THE GENERATE_SEMICIRCLE FUNCTION SO THAT HERE I CAN GENERATE A SEMICIRCLE WITH THE DIAMETER THE STRAIGHT LINE BETWEEN
        # START AND END POINTS, WHICH CAN BE ADJUSTED. I WILL CREATE A CONSTANT FOR THE CENTRE OF THE SEMICIRCLE, WHICH CAN BE USED EITHER
        # WHEN THE ROUTE RETURNS TO THE START OR IT REACHES A DIFFERENT FINAL DESTINATION
        nothing = 0
    
    waypoints_addresses = []
    for waypoint in waypoints:
        waypoints_addresses.append(gmaps.reverse_geocode(latlng=(str(waypoint[0]) + "," + str(waypoint[1])))[0]["formatted_address"])
    ### Converts all waypoints into addresses for the directions to use
    
    
    
    results = gmaps.directions(origin = gmaps.geocode(kwargs["start_location"])[0]["formatted_address"], 
                                         destination = gmaps.geocode(kwargs["end_location"])[0]["formatted_address"],                
                                         waypoints = waypoints_addresses,
                                         mode = kwargs["travel_method"],
                                         optimize_waypoints = True,
                                         departure_time=datetime.datetime.now())
    ### Takes the start and end location and the added waypoints and makes a route


    return results






start_location = input("Your Address")
if input("Would you like to return to here?") == "yes":
    end_location = start_location
else: 
    end_location = input("Ending Address")
if input("Would you like to find a route by time or distance?") == "distance":
    distance = float(input("What distance would you like to travel in kilometers?"))### NO MORE THAN 1 DECIMAL PLACE: ADD INPUT VALIDATION FOR ALL INPUTS
    distance *= 1000.0
    distance = int(distance)
    time = ""
else:
    time = int(input("How long would you like to travel for in minutes?"))
    distance = ""
travel_method = input("Would you like to travel by walking, bicycling, or running?")
### Takes the information about the route from the user


route_complete = False 
### Route is completely formed to the information given


lngr = ""
### Flag for if the route needs to be longer or shorter, later a boolean, empty string means no route calculated yet

global start_coordinates, end_coordinates,average_coordinates,times_changed,waypoints,radius
radius = 0.0
waypoints = []
times_changed = 0
start_coordinates = gmaps.geocode(start_location)[0]["geometry"]["viewport"]["northeast"] ### Gets coordinates for start and end
start_coordinates = [start_coordinates["lat"],start_coordinates["lng"]] ### Converts to a list [latitude,longitude]
end_coordinates = gmaps.geocode(start_location)[0]["geometry"]["viewport"]["northeast"]
end_coordinates = [end_coordinates["lat"],end_coordinates["lng"]] ### Converts to a list [latitude,longitude]
average_coordinates = [(start_coordinates[0] + end_coordinates[0]/2),
                        (start_coordinates[1] + end_coordinates[1]/2)] ### Calculates the middle point between start and end
### average_coordinates creates a centre to work from. If the route needs to be longer, the waypoints are moved away from the centre. If it needs
### to be shorter, they are moved towards the centre


if end_location == start_location:
    for x in range(5):
        waypoints.append(start_coordinates) 
### Adds 5 waypoints at the start/end point to be changed later


else:
    waypoints.append(start_coordinates)
    waypoints.append([(start_coordinates["lat"] + average_coordinates["lat"]/2),
                        (start_coordinates["lng"] + average_coordinates["lng"]/2)])
    waypoints.append(average_coordinates)
    waypoints.append([(average_coordinates["lat"] + end_coordinates["lat"]/2),
                        (average_coordinates["lng"] + end_coordinates["lng"]/2)])
    waypoints.append(end_coordinates)
    ### Adds 5 waypoints between start and end to be changed later, if the start point is not the same as the end point
      


while not route_complete:
    ### Generate different routes until one matches the information given
    
    
    results = generate_route(start_location=start_location,
                            end_location=end_location,
                            distance=distance,
                            time=time,
                            travel_method=travel_method,
                            longer=lngr)
    ### Uses the function to generate a route with waypoints


    times_changed += 1
    ### Iterates the flag for number of times the route has been made or changed by one(global)


    route_distance = 0 
    for leg in results[0]["legs"]: 
        leg_distance = leg["distance"]["text"]
        if "km" in leg_distance:
            leg_distance = float(leg_distance[:-2])*1000
        else:
            leg_distance = float(leg_distance[:-1])*1000
        route_distance += leg_distance
    route_distance = int(route_distance)
    print(route_distance,"m")
    ### Calculates the distance of the returned route


    route_time = 0 
    for leg in results[0]["legs"]: 
        leg_time = leg["duration"]["text"]
        leg_time = int(leg_time[:-4])
        route_time += leg_time
    route_time = int(route_time)
    print(route_time,"mins")
    ### Calculates the time of the returned route


    if distance != "":
        if route_distance == distance:
            pprint(results)
            break
        elif route_distance < distance:
            lngr = True
        else:
            lngr = False
    ### If user input distance, checks if the route needs to be longer or shorter
    


    else:
        if route_time == time:
            pprint(results)
            break
        elif route_time < time:
            lngr = True
        else:
            lngr = False
    ### If user input time, checks if the route needs to be longer or shorter








