#!/usr/bin/env python

__author__ = "Jordan Haagenson"

# Import packages
import requests
import io
import turtle
import datetime
import time





# Create global variables
# printer = pprint.pprint
astros_API = 'http://api.open-notify.org/astros.json'
iss_now_API = 'http://api.open-notify.org/iss-now.json'
nasa_check_iss = 'https://spotthestation.nasa.gov/tracking_map.cfm'
next_pass = 'http://api.open-notify.org/iss-pass.json'
indiana_lat, indiana_lon = indiana_coords = 39.76, -86.159
bg = 'map.gif'
iss_icon = 'iss.gif'


def get_request_to_dict(url):
    """
    Returns a dictionary of response to get request of url provided.
    :param url: str
    :return: dict
    """
    response = requests.get(url)
    d = response.json()
    return d


def time_convert(timestamp):
    """
    Takes in a time stamp and converts it to a human-readable form
    :param timestamp: int
    :return: datetime object
    """
    return time.ctime(timestamp)


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
        print(f"{i['name']} aboard the {i['craft']}")
    return


def find_iss_location():
    """
    Gets current iss location at current time
    :return: dict
    """
    current = get_request_to_dict(iss_now_API)
    return current


def setup_screen(bg_img):
    """
    Creates a turtle screen, displays a background image, and sets world coords
    :param bg_img:
    :return: window
    """
    screen = turtle.Screen()
    # screen = turtle.Screen()
    screen.setworldcoordinates(-180, -90, 180, 90)
    screen.mode('world')
    screen.bgpic(bg_img)
    screen.update()
    return screen


def setup_pen(img):
    """
    Sets icon of pen object for turtle screen
    :param img: image file name
    :type img: str
    :return:pen
    """
    turtle.addshape(img)
    pen = turtle.getpen()
    pen.shape(img)
    return pen


def goto_iss(screen, pen, longitude, latitude):
    """
    Move icon to current iss location
    :param pen: turtle pen object
    :param longitude: float
    :param latitude: float
    :return: pen
    """
    pen.penup()
    pen.goto(longitude, latitude)
    screen.update()
    return pen


def next_indie_pass(current_lat, current_lon):
    """
    Draw a dot on next flyover of Indianapolis
    :param current_lat: int or float
    :param current_lon: int or float
    :return:map of world
    """
    response = requests.get(next_pass + "?lat=" + str(current_lat) + "&lon="+str(current_lon))
    r = response.json()
    time.ctime()
    return r


def test_iss_location(iss_location):
    nasa = requests.get(nasa_check_iss)
    return iss_location == nasa


def main():
    print("Part A\n")
    astronauts = get_request_to_dict(astros_API)
    print_in_orbit(astronauts)
    
    print("Part B\n")
    current = find_iss_location()
    long = current['iss_position']['longitude']
    lat = current['iss_position']['latitude']
    test = test_iss_location(current)

    print("Part C\n")
    window = setup_screen(bg)
    pen = setup_pen(iss_icon)
    goto_iss(window, pen, long, lat)

    print("Part D\n")
    next_indie_pass(39.76, -86.159)

if __name__ == '__main__':
    main()
