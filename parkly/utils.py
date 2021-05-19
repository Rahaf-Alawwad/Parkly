from django.contrib.gis.geoip2 import  GeoIP2

def get_geo(ip):
    geo = GeoIP2()
    country=geo.country(ip)
    city=geo.city(ip)
    lat,lang = geo.lat_lon(ip)
    return country, city, lat,lang

def get_coordinates(latLocation, longLocation, latDestination=None, longDestination=None):
    coordinates =(latLocation,longLocation)
    if latDestination:
        coordinates=[(latLocation+latDestination)/2, (longLocation+longDestination)/2]
    return coordinates

def get_zoom(distance):
    if distance <= 100:
        return 10
    elif distance > 100 and distance< 5000:
        return 4
    else:
        return 2