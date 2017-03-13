"""
Geocoding and Web APIs Project Toolbox exercise

Find the MBTA stops closest to a given location.

Full instructions are at:
https://sites.google.com/site/sd15spring/home/project-toolbox/geocoding-and-web-apis
"""
import mbta_finder
from urllib.request import urlopen
import json
from pprint import pprint


# Useful URLs (you need to add the appropriate parameters for your requests)
GMAPS_BASE_URL = "https://maps.googleapis.com/maps/api/geocode/json"
MBTA_BASE_URL = "http://realtime.mbta.com/developer/api/v2/stopsbylocation"
MBTA_DEMO_API_KEY = "wX9NwuHnZU2ToO7GmGR9uw"


# A little bit of scaffolding if you want to use it

def get_json(url):
    """
    Given a properly formatted URL for a JSON web API request, return
    a Python JSON object containing the response to that request.
    """
    f = urlopen(url)
    response_text = f.read()
    response_data = json.loads(str(response_text, 'utf-8'))
    # pprint(response_data)
    return response_data

url = "https://maps.googleapis.com/maps/api/geocode/json?address=Fenway%20Park"
get_json(url)



def get_lat_long(place_name):
    """
    Given a place name or address, return a (latitude, longitude) tuple
    with the coordinates of the given place.

    See https://developers.google.com/maps/documentation/geocoding/
    for Google Maps Geocode API URL formatting requirements.
    """
    separations_place_name = place_name.split()
    symbols = ''
    # Replace the spaces in between the address with '+' for the url
    for i in separations_place_name:
        symbols = symbols + i
        symbols = symbols + '+'
    symbols = symbols[0:-1]

    MY_API_KEY = 'AIzaSyBr3ULSrrWGYsxmtE-4eA4SH1wB17rQIhE'
    url = 'https://maps.googleapis.com/maps/api/geocode/json?address='
    final_url = url + symbols + '&key=' + MY_API_KEY
    response_data = get_json(final_url)
    latitude = response_data["results"][0]["geometry"]["location"]["lat"]
    longitude = response_data["results"][0]["geometry"]["location"]["lng"]
    return latitude, longitude

get_lat_long('Fenway Park')


def get_nearest_station(latitude, longitude):
    """
    Given latitude and longitude strings, return a (station_name, distance)
    tuple for the nearest MBTA station to the given coordinates.

    See http://realtime.mbta.com/Portal/Home/Documents for URL
    formatting requirements for the 'stopsbylocation' API.
    """
    url = 'http://realtime.mbta.com/developer/api/v2/stopsbylocation?api_key=wX9NwuHnZU2ToO7GmGR9uw'
    specific_location = '&lat=' + str(latitude) + '&lon=' + str(longitude) + '&format=json'
    final_url = url + specific_location
    response_data = get_json(final_url)
    nearby_station = response_data["stop"][0]["stop_name"]
    distance = response_data["stop"][0]["distance"]
    """if float(distance) < 1:
        distance = float(distance) / 5280
        distance = str(distance)"""
    return nearby_station, distance


def find_stop_near(place_name):
    """
    Given a place name or address, print the nearest MBTA stop and the
    distance from the given place to that stop.
    """
    user_input = input('Please enter a location you would like to search: \n')
    latitude, longitude = get_lat_long(user_input)
    # latitude = str(coordinates[0])
    # longitude = str(coordinates[1])
    nearest = get_nearest_station(latitude, longitude)
    print('The nearest station is ' + str(nearest[0]) + ' which is ' + str(nearest[1]) + ' miles away.')
    return nearest

if __name__ == '__main__':
    latitude, longitude = get_lat_long('Fenway Park')
    get_nearest_station(latitude, longitude)
    find_stop_near('Fenway Park')
