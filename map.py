import folium
from geopy.geocoders import Nominatim
from haversine import haversine
from geopy.extra.rate_limiter import RateLimiter
from geopy.exc import GeocoderUnavailable

my_map = folium.Map()
geolocator = Nominatim(user_agent="map.py")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=0.5)



def check_elem(elem):
    if elem != '':
        return True
    return False

def find_year(year,coords):
    """
    (['Film20', '2020', 'Sydney'], 15201.042185096521, (-33.8548157, 151.2164539))
    """
    line_number = 1
    result =[]
    with open("locations.list", 'r') as locations:
        for line in locations:
            # try:
            if (year in line) and 14 < line_number <= 1100000: #1241786 :
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
                    # print(line_number)
                    print(0,line_number)
            # except GeocoderUnavailable:
            #     print(1,line_number)
            # elif line_number > 1000000:
            #     break
            line_number += 1
    result.sort(key=lambda x : x[1])
    
    return result



if __name__ == "__main__":
    print("Welcome to our programm!")
    year = input("Please enter a year you would like to have a map for:")
    user_lat, user_long = 0,0 #input("Please enter your location (format: lat, long):").split(",")
    user_coords = (user_lat,user_long)
    films_in_needed_year = find_year(year,user_coords)
    # print(films_in_needed_year)
    for i in range(10):
        if i >= len(films_in_needed_year):
            break
        my_map.add_child(folium.Marker(location=[films_in_needed_year[i][2][0],films_in_needed_year[i][2][1]], popup= films_in_needed_year[i][0], icon = folium.Icon( color="green", icon_color="yellow", icon="camera")))
    my_map.add_child(folium.Marker(location=[user_lat,user_long], popup= "You are here!", icon = folium.Icon( color="red", icon_color="white", icon = "home")))
    # my_map.add_child(folium.vector_layers.Circle(location=[user_lat,user_long], radius = films_in_needed_year[0][1]*1000))
    my_map.add_child(folium.features.ClickForMarker(popup="HELLO"))
    my_map.save("map.html")
    print(len(films_in_needed_year))