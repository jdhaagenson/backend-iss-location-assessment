#!/usr/bin/env python

__author__ = "Jordan Haagenson"


##
# Import packages
import requests
import turtle
import time

##
# Create global variables
astros_API = 'http://api.open-notify.org/astros.json'
iss_now_API = 'http://api.open-notify.org/iss-now.json'
next_pass = 'http://api.open-notify.org/iss-pass.json'
indiana_lat, indiana_lon = 39.76, -86.159
bg = 'map.gif'
iss_icon = 'iss.gif'


##
def get_request_to_dict(url):
    """
    Returns a dictionary of response to get request of url provided.
    :param url: str
    :return: dict
    """
    response = requests.get(url)
    d = response.json()
    return d


##
def time_convert(timestamp):
    """
    Takes in a time stamp and converts it to a human-readable form
    :param timestamp: int
    :return: datetime object
    """
    return time.ctime(int(timestamp))


##
def print_in_orbit(dictionary):
    """
    Print out number of astronauts currently in orbit, their names and what 
    craft they are aboard.
    :param dictionary:
    :return:
    """
    people = dictionary['people']
    print('Astronauts in currently in space: ', dictionary['number'])
    for i in people:
        print(f"{i['name']}; {i['craft']}")
    return


##
def find_iss_location():
    """
    Gets current iss location at current time
    :return: dict
    """
    current = get_request_to_dict(iss_now_API)
    return current


##
def setup(bg_img=bg):
    """
    Creates a turtle screen, displays a background image, and sets world coords
    :param bg_img:
    :return: window
    """
    # turtle.register_shape(img)
    screen = turtle.Screen()
    screen.setup(width=720, height=360, startx=0, starty=0)
    screen.setworldcoordinates(-180, -90, 180, 90)
    turtle.mode('world')
    screen.bgpic(bg_img)
    # pen = turtle.Turtle(shape=img)
    return screen


##
def goto_iss(longitude, latitude, indiana=False):
    """
    Move pen to coordinates provided
    :param longitude: longitude
    :type longitude: float
    :param latitude: latitude
    :type latitude: float
    :param indiana: when False (default) goto_coord will move ISS
    :type indiana: bool
    :return: pen
    :rtype: <class 'turtle.Turtle'>
    """
    if not indiana:
        turtle.register_shape(iss_icon)
        pen = turtle.Turtle(shape=iss_icon)
        pen.penup()
        pen.setpos(float(longitude), float(latitude))
        return pen
    if indiana:
        pen = turtle.Turtle(visible=False)
        pen.penup()
        pen.color('yellow')
        pen.setpos(float(longitude), float(latitude))
        pen.dot(10, 'yellow')
        return pen


##
def mark_indiana(timestamp=None):
    """
    Marks Indianapolis with a yellow dot and writes time of next
    pass over if timestamp is specified
    :param timestamp: converted timestamp of next passover of Indianapolis
    :type timestamp: str
    """
    pen = goto_iss(indiana_lon, indiana_lat, indiana=True)
    print(indiana_lon, indiana_lat)
    if timestamp is not None:
        pen.write(timestamp, align="right", font=('Courier New', 10, 'bold'))


##
def next_indie_pass():
    """
    Gets the next pass over timestamp, converts it, and passes it to mark_indiana() function to write it to the screen
    """
    response = requests.get(next_pass + "?lat=39.76&lon=-86.159")
    response = response.json()
    t = response['response'][0]['risetime']
    tme = time_convert(t)
    print("Next passover of Indianapolis, Indiana will occur on:")
    print(tme)
    return mark_indiana(tme)


##
def main():
    print("Obtain full names of every astronaut currently in orbit and the name of their craft")
    astronauts = get_request_to_dict(astros_API)
    print_in_orbit(astronauts)
    print("Current location where the International Space Station is currently orbiting:")
    current = find_iss_location()
    print(current['iss_position'])
    long = current['iss_position']['longitude']
    lat = current['iss_position']['latitude']
    setup()
    goto_iss(longitude=long, latitude=lat)
    next_indie_pass()
    turtle.Screen().exitonclick()


##
if __name__ == '__main__':
    main()


