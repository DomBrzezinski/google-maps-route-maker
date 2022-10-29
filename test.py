import math as maths

start_coordinates = [6,7]
end_coordinates = [13,14]
waypoints = [[],[],[],[],[]]

global center_of_semicircle

direct_distance = maths.sqrt(((end_coordinates[0] - start_coordinates[0])**2)+((end_coordinates[1] - start_coordinates[1])**2))
center_of_semicircle = [((end_coordinates[0]-start_coordinates[0])/2)+start_coordinates[0],((end_coordinates[1]-start_coordinates[1])/2)+start_coordinates[1]]
center_of_semicircle = list(center_of_semicircle)

def rotate(coordinates):
    x1 = (maths.cos(maths.pi/4)*(coordinates[0] - center_of_semicircle[0])) + (maths.sin(maths.pi/4)*(coordinates[1] - center_of_semicircle[1]))
    y1 = -1*(maths.sin(maths.pi/4)*(coordinates[0] - center_of_semicircle[0])) + (maths.cos(maths.pi/4)*(coordinates[1] - center_of_semicircle[1]))
    x1 = x1 + center_of_semicircle[0]
    y1 = y1 + center_of_semicircle[1]
    return [x1,y1]

waypoints[0] = start_coordinates

waypoints[1] = rotate(waypoints[0])

waypoints[2] = rotate(waypoints[1])

waypoints[3] = rotate(waypoints[2])

waypoints[4] = end_coordinates


with open("test.txt","a") as f:
    for item in waypoints:
        f.write(str(item[0]))
        f.write(", ")
        f.write(str(item[1]))
        f.write("\n")