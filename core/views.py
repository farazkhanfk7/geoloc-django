from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from . models import Measurement
from . forms import MeasurementForm
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from .utils import get_geo,get_center_coordinates,get_zoom_value,get_ip_address
import folium

# Create your views here.
def home(request):
    if request.method=='POST':
        obj = get_object_or_404(Measurement,id=1)
        form = MeasurementForm(request.POST or None)
        geolocator = Nominatim(user_agent='core')

        #to get realtime ip-address once deployed
        # ip = get_ip_address(request)
        # print(ip)

        ip='139.167.230.131' #delhi central kotwali tehsil
        _country, city, lat, lon = get_geo(ip)
        # print(f'{city},{country} and lat-log:{lat}:{lon}')

        location = geolocator.geocode(city)
        # print(f'Detailed location via geocode : {location}')

        #location coordinates
        l_lat = lat
        l_lon = lon
        point_a = (l_lat,l_lon)

        if form.is_valid():
            instance = form.save(commit=False)
            destination_ = form.cleaned_data.get('destination')
            destination = geolocator.geocode(destination_)
            # print(destination)

            #destination coordinates
            d_lat = destination.latitude
            d_lon = destination.longitude
            point_b = (d_lat,d_lon)

            #calculate distance  
            distance = round(geodesic(point_a,point_b).km,2)

            #revised folium map
            center_coordinates = get_center_coordinates(l_lat,l_lon,d_lat,d_lon)
            m = folium.Map(width=800,height=500,location=center_coordinates,zoom_start=get_zoom_value(distance))
            #location marker
            folium.Marker([l_lat,l_lon],tooltip='click here for more',popup=city['city'],icon=folium.Icon(color='purple')).add_to(m)
            #destination marker
            folium.Marker([d_lat,d_lon],tooltip='click here for more',popup=destination,icon=folium.Icon(color='red')).add_to(m)
            #draw line
            line = folium.PolyLine(locations=[point_a,point_b],weight=5,color='blue',popup=f'Distance: {distance} km')
            m.add_child(line)
            m = m._repr_html_()

            #save to form         
            instance.location = location
            instance.distance = distance
            instance.save()

        context = {
            'distance':obj,
            'form': form,
            'map':m
        }

        return render(request,'main.html',context)
    else:
        geolocator = Nominatim(user_agent='core')
        #to get realtime ip-address once deployed
        # ip = get_ip_address(request)
        # print(ip)
        #getting initial location
        ip='139.167.230.131' #delhi central kotwali tehsil
        _country, city, lat, lon = get_geo(ip)
        # print(f'{city},{country} and lat-log:{lat}:{lon}')

        location = geolocator.geocode(city)
        # print(f'Detailed location via geocode : {location}')

        #location coordinates
        l_lat = lat
        l_lon = lon
        point_a = (l_lat,l_lon)

        #initial folium map
        m = folium.Map(width=800,height=500,location=point_a,zoom_start=10)
        folium.Marker([l_lat,l_lon],tooltip='click here for more',popup=city['city'],icon=folium.Icon(color='purple')).add_to(m)
        m = m._repr_html_()

        form = MeasurementForm()
        context = {
            'form': form,
            'map' : m
        } 
        return render(request,'main.html',context)