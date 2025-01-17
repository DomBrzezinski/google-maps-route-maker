### This program generates a running, cycling or walking route from a distance or length of time given by the user
### 1 degree of latitude is the 111,139 meters
import googlemaps
import datetime
import math as maths
from pprint import pprint
import os

API_KEY = str(open(os.path.dirname(os.path.realpath(__file__)) + '\\key.txt', "r").readline())
gmaps = googlemaps.Client(key=API_KEY)
### Receives the Google Maps Client to send requests to

def distance_calculator(start,end):
    return maths.sqrt(((end['lat'] - start['lat'])**2)+((end['lng'] - start['lng'])**2))


def rotate(coordinates):
    """
    Rotates points about center of the semicircle by taking away the distance to the origin rotating about the origin with a matrix transformation
    This rotates by 90 degrees anticlockwise, and adds on the distance taken away at the end
    """
    x1 = (maths.cos(maths.pi/6)*(coordinates[0] - center_of_semicircle[0])) + (maths.sin(maths.pi/6)*(coordinates[1] - center_of_semicircle[1]))
    y1 = -1*(maths.sin(maths.pi/6)*(coordinates[0] - center_of_semicircle[0])) + (maths.cos(maths.pi/6)*(coordinates[1] - center_of_semicircle[1]))
    x1 = x1 + center_of_semicircle[0]
    y1 = y1 + center_of_semicircle[1]
    return [x1,y1]



def route_output(results, distance, time):
    """
    Prints out the results of a directions request in a user friendly way
    INPUT:
            Route information, total distance of route, total time of route
    OUTPUT:
            Prints the route and points along the way, with leg times and distances
    """
    for i, leg in enumerate(results[0]["legs"]):
        print("Stop:" + str(i),
            leg["start_address"], 
            "==> ",
            leg["end_address"], 
            "distance: ", 
            str(leg["distance"]["value"]) + "m", 
            "traveling Time:",
            str(leg["duration"]["value"])[:-1] + "s"
        )
    print("total distance:",str(distance) + "m" )
    print("total time:",str(time) + "mins" )


def generate_semicircle(**kwargs):
    """
    Generates a semicicle or semi-ellipse of given radius at the start coordinates. Can stretch existing semi-circle or semi-ellipse to increase/
    decrease distance
    INPUT: 
            Both vertices of the semicircle, or semi-ellipse as a global variable as well as the stretch factor to apply(in kwargs)
    OUTPUT: 
            Waypoints(global variable)
    """
    global radius
    print(start_coordinates, end_coordinates)
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
        radius = direct_distance/2
        global center_of_semicircle
        center_of_semicircle = [((end_coordinates[0]-start_coordinates[0])/2)+start_coordinates[0],((end_coordinates[1]-start_coordinates[1])/2)+start_coordinates[1]]
        ### Finds the direct gradient and distance between start and end, and finds the centre of the semicircle

        
        waypoints[0] = rotate(start_coordinates)

        waypoints[1] = rotate(waypoints[0])

        waypoints[2] = rotate(waypoints[1])

        waypoints[3] = rotate(waypoints[2])

        waypoints[4] = rotate(waypoints[3])
        ### This creates the normal curve semicircle based on the direct distance between points, can be returned and checked and stretched
        

        if kwargs["stretch"] != 0:
            perpendicular_gradient = -1/direct_gradient
            if start_coordinates[1] > end_coordinates[1]:
                x_changer = 1
            else:
                x_changer = -1
            if start_coordinates[0] > end_coordinates[0]:
                y_changer = -1
            else:
                y_changer = 1
            ### This creates the flags for if the program is to add or subtract a set value of x and y from the previous point, in order to stretch the
            ### point from the direct line between start and end. This finds the direction to stretch (positive/negative x and y).
            ### Start position in terms of the points being input is the opposite(waypoints[5] is the start, as it goes anticlockwise in the rotation),
            ### so thats why the values may appear to be switched around


            stretch = kwargs["stretch"]
            angle = maths.atan(abs(perpendicular_gradient))
            ### Unpacks the stretching factor and gets the absolute value of the angle of the line in radians


            waypoints[1] = [waypoints[1][0] + x_changer*(stretch-1)*radius*maths.cos(angle), waypoints[1][1] + y_changer*(stretch-1)*radius*maths.sin(angle)]
            waypoints[2] = [waypoints[2][0] + x_changer*(stretch-1)*radius*maths.cos(angle), waypoints[2][1] + y_changer*(stretch-1)*radius*maths.sin(angle)]
            waypoints[3] = [waypoints[3][0] + x_changer*(stretch-1)*radius*maths.cos(angle), waypoints[3][1] + y_changer*(stretch-1)*radius*maths.sin(angle)]
            ### Adds to the existing point the proportional stretch from the direct distance line. x_changer makes it go in the right direction, stretch-1
            ### is to get the added part of the stretch on top of the original, this is multiplied by the radius, to make it proportional to the circle,
            ### and the angle is used to make it add in the right direction
        
        
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
            if kwargs["distance"] != "":
                radius = (kwargs["distance"]/(maths.pi + 2.0))/1.2
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
            print(kwargs["longer"])
            if kwargs["longer"]:
                radius *= 1.2
            else:
                radius /= 1.3
        generate_semicircle()
    ### Makes a semicircular route with adjusted radius based on the "longer" key
    

    else:
        global stretcher
        if times_changed != 0:
            if kwargs["longer"]:
                previous_stretch = stretcher
                stretcher = previous_stretch * 1.2
                generate_semicircle(stretch = stretcher)
            else:
                previous_stretch = stretcher
                stretcher = previous_stretch / 1.3
                generate_semicircle(stretch = stretcher)     
        else:
            stretcher = 1
            generate_semicircle(stretch = 0)
        nothing = 0
    

    waypoints_addresses = []
    for waypoint in waypoints:
        waypoints_addresses.append(gmaps.reverse_geocode(latlng=(str(waypoint[0]) + "," + str(waypoint[1])))[0]["formatted_address"])
    ### Converts all waypoints into addresses for the directions to use
    

    results = gmaps.directions(origin = gmaps.geocode(kwargs["start_location"])[0]["formatted_address"], 
                                         destination = gmaps.geocode(kwargs["end_location"])[0]["formatted_address"],                
                                         waypoints = waypoints_addresses,
                                         mode = kwargs["travel_method"],
                                         optimize_waypoints = False,
                                         departure_time=datetime.datetime.now())
    ### Takes the start and end location and the added waypoints and makes a route


    return results,waypoints_addresses

def route_main(base_inputs):

    global start_coordinates, end_coordinates,average_coordinates,times_changed,waypoints


    start_location = base_inputs["starting_location"]
    end_location = base_inputs["ending_location"]
    return_original = base_inputs["return_original"]
    travel_method =  base_inputs["travel_method"].lower()
    time =  base_inputs["time_input"]
    distance = base_inputs["distance_input"]
    time_or_distance = base_inputs["time_or_distance"]

    if time_or_distance == "1": distance = ""
    else: time = ""

    if distance != "":
        distance *= 1000.0
        distance = int(distance)

    if return_original:
        end_location = start_location

    
    start_coordinates = gmaps.geocode(start_location)[0]["geometry"]["bounds"]["northeast"]
    end_coordinates = gmaps.geocode(end_location)[0]["geometry"]["bounds"]["northeast"]
    start_coordinates = [start_coordinates["lat"],start_coordinates["lng"]] ### Converts to a list [latitude,longitude]
    end_coordinates = [end_coordinates["lat"],end_coordinates["lng"]] ### Converts to a list [latitude,longitude]


    # accept = False
    # while not accept:
    #     accept = True
    #     start_location = input("Your Address ")
    #     start_coordinates = gmaps.geocode(start_location)
    #     if start_coordinates ==  []: 
    #         print("Invalid Address")
    #         accept = False
    #     else: start_coordinates = start_coordinates[0]["geometry"]["viewport"]["northeast"] ### Gets coordinates for start and end
            
    # accept = False
    # while not accept:
    #     accept = True
    #     return_input = input("Would you like to return to here? ")    
    #     if return_input == "yes":
    #         end_location = start_location
    #         end_coordinates = start_coordinates
    #     elif return_input == "no": 
    #         accept_ = False
    #         while not accept_:
    #             end_location = input("Ending Address ")
    #             try:
    #                 end_coordinates = gmaps.geocode(end_location)[0]["geometry"]["viewport"]["northeast"] ### Gets coordinates for start and end
    #                 m_distance = distance_calculator(start_coordinates,end_coordinates) * 111139.0
    #                 print(m_distance)
    #                 if m_distance > 500000:
    #                     print("too long")
    #                     accept_ = False
    #                 accept_ = True
    #             except: accept_ = False            
    #     else: accept = False
        
    # start_coordinates = [start_coordinates["lat"],start_coordinates["lng"]] ### Converts to a list [latitude,longitude]
    # end_coordinates = [end_coordinates["lat"],end_coordinates["lng"]] ### Converts to a list [latitude,longitude]
    # accept = False
    # while not accept:
    #     travel_method = input("Would you like to travel by walking, bicycling, or running? ")
    #     if travel_method == "walking" or travel_method == "bicycling" or travel_method == "running":
    #         accept = True

    # accept = False
    # while not accept:
    #     accept = True
    #     time_distance = input("Would you like to find a route by time or distance? ")
    #     if time_distance == "distance":
    #         accept_ = False
    #         while not accept_:
    #             accept_ = True
    #             distance = input("What distance would you like to travel in kilometers? ")### NO MORE THAN 1 DECIMAL PLACE: ADD INPUT VALIDATION FOR ALL INPUTS
    #             try:
    #                 distance = float(distance)
    #                 distance *= 1000.0
    #                 distance = int(distance)
    #                 time = ""
    #                 if return_input == "no":
    #                     if m_distance > distance*0.7:
    #                         print("too short")
    #                         accept_ = False
    #             except: accept_ = False
    #     elif time_distance == "time":
    #         accept_ = False
    #         while not accept_:
    #             accept_ = True
    #             time = input("How long would you like to travel for in minutes? ")
    #             try:
    #                 time = int(time)
    #                 distance = ""
    #                 if travel_method == "walking":
    #                     if time < (m_distance/84)*0.7:
    #                         print("too short")
    #                         a = "a" + 4
    #                 elif travel_method == "bicycling":
    #                     if time < (m_distance/420)*0.7:
    #                         print("too short")
    #                         a = "a" + 4
    #                 elif travel_method == "running":
    #                     if time < (m_distance/300)*0.7:
    #                         print("too short")
    #                         a = "a" + 4
    #             except: accept_ = False
    #     else:
    #         accept = False


    ### Takes the information about the route from the user


    route_complete = False ### Route is completely formed to the information given
    lngr = "" ### Flag for if the route needs to be longer or shorter, later a boolean, empty string means no route calculated yet

    radius = 0.0
    waypoints = []
    times_changed = 0

    if end_location == start_location:
        for x in range(5):
            waypoints.append(start_coordinates) 
    ### Adds 5 waypoints at the start/end point to be changed later


    else:
        average_coordinates = [(start_coordinates[0] + end_coordinates[0])/2,
                                (start_coordinates[1] + end_coordinates[1])/2] ### Calculates the middle point between start and end
        ### average_coordinates creates a centre to work from. If the route needs to be longer, the waypoints are moved away from the centre. If it needs
        ### to be shorter, they are moved towards the centre
        waypoints.append(start_coordinates)
        waypoints.append([(start_coordinates[0] + average_coordinates[0]/2),
                            (start_coordinates[1] + average_coordinates[1]/2)])
        waypoints.append(average_coordinates)
        waypoints.append([(average_coordinates[0] + end_coordinates[0]/2),
                            (average_coordinates[1] + end_coordinates[1]/2)])
        waypoints.append(end_coordinates)
        ### Adds 5 waypoints between start and end to be changed later, if the start point is not the same as the end point
        


    while not route_complete:
        ### Generate different routes until one matches the information given
        

        results, returned_waypoints = generate_route(start_location=start_location,
                                end_location=end_location,
                                distance=distance,
                                time=time,
                                travel_method=travel_method,
                                longer=lngr)
        ### Uses the function to generate a route with waypoints

        times_changed += 1
        ### Iterates the flag for number of times the route has been made or changed by one(global)
        # pprint(results) ### HERE PRODUCES AN EMPTY LIST FSR, IDK WHY, CHECK THIS OUT
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
                route_output(results, route_distance, route_time)
                route_complete = True
            elif route_distance < distance:
                lngr = True
            else:
                lngr = False
        ### If user input distance, checks if the route needs to be longer or shorter
        


        else:
            if route_time == time:
                route_output(results, route_distance, route_time)
                route_complete = True
            elif route_time < time:
                lngr = True
            else:
                lngr = False
        ### If user input time, checks if the route needs to be longer or shorter
    return [returned_waypoints, waypoints, travel_method, start_coordinates, end_coordinates, route_distance, route_time]
