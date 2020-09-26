from django.contrib.gis.geoip2 import GeoIP2

#Helper fuctions
def get_geo(ip):
    g = GeoIP2()
    country = g.country(ip)
    city = g.city(ip)
    lat, lon = g.lat_lon(ip)
    return country, city, lat, lon

def get_center_coordinates(lat_a,lon_a,lat_b,lon_b):
    cord = [(lat_a+lat_b)/2,(lon_a+lon_b)/2]
    return cord

def get_ip_address(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_zoom_value(distance):
    if distance <= 100:
        return 8
    elif distance>100 and distance<=5000:
        return 4
    else:
        return 2

    #will be using this to get proper map zoom value according to the distance.
    #to be used in folium.Map
