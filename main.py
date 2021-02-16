""" Github: https://github.com/taarsikis/find_near_film """

import folium
from haversine import haversine
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from geopy.exc import GeocoderUnavailable

my_map = folium.Map()
geolocator = Nominatim(user_agent="main.py")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=0.5)



def check_elem(elem):
    """ Check is this element '' or not """
    if elem != '':
        return True
    return False

def find_year(year,coords):
    """
    Checks locations.list file and returns list of films, filmed in needed year.
    Returns: (film, distanse to user coords, film coords)
    """
    line_number = 1
    result =[]
    with open("locations.list", 'r') as locations:
        for line in locations:
            try:
                if (year in line) and 14 < line_number <= 1241786 :
                    line_lst = line[:-1].split("\t")
                    line_lst = list(filter(check_elem, line_lst))
                    try:
                        if ")" not in line_lst[-1]:
                            location = geolocator.geocode(line_lst[-1])
                        else:
                            location = geolocator.geocode(line_lst[-2])
                        film_coords = (location.latitude,location.longitude)
                        distance = haversine(coords,film_coords)
                        line_lst[0] = line_lst[0].split("(")
                        film_name = line_lst[0][0]

                        result.append((film_name,distance, film_coords))
                    except AttributeError:
                        pass
            except GeocoderUnavailable:
                pass
            line_number += 1
    result.sort(key=lambda x : x[1])

    return result



if __name__ == "__main__":
    print("Welcome to our programm!")

    year = input("Please enter a year you would like to have a map for:")
    user_lat, user_long = input("Please enter your location (format: lat, long):").split(",")
    user_lat = int(user_lat)
    user_long = int(user_long)

    print("Please, wait!")

    user_coords = (user_lat,user_long)
    films_in_needed_year = find_year(year,user_coords)

    for i in range(10):
        if i >= len(films_in_needed_year):
            break
        my_map.add_child(folium.Marker(location=[films_in_needed_year[i][2][0],\
films_in_needed_year[i][2][1]], \
popup= films_in_needed_year[i][0], \
icon = folium.Icon( color="green", icon_color="yellow", icon="camera")))
    my_map.add_child(folium.Marker(location=[user_lat,user_long], popup= "You are here!", \
        icon = folium.Icon( color="red", icon_color="white", icon = "home")))

    my_map.add_child(folium.features.ClickForMarker(popup="HELLO"))
    my_map.save("map.html")

    print("Results are in \" map.html \"")
