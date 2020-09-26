from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from . models import Measurement
from . forms import MeasurementForm
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from .utils import get_geo

# Create your views here.
def home(request):
    if request.method=='POST':
        obj = get_object_or_404(Measurement,id=1)
        form = MeasurementForm(request.POST or None)
        geolocator = Nominatim(user_agent='core')

        ip='139.167.230.131' #delhi central kotwali tehsil
        country, city, lat, lon = get_geo(ip)
        # print(f'{city},{country} and lat-log:{lat}:{lon}')

        location = geolocator.geocode(city)
        # print(f'Detailed location via geocode : {location}')

        l_lat = lat
        l_lon = lon
        point_a = (l_lat,l_lon)

        if form.is_valid():
            instance = form.save(commit=False)
            destination_ = form.cleaned_data.get('destination')
            destination = geolocator.geocode(destination_)
            # print(destination)
            d_lat = destination.latitude
            d_lon = destination.longitude

            point_b = (d_lat,d_lon)  
            distance = round(geodesic(point_a,point_b).km,2)         
            instance.location = location
            instance.distance = distance
            instance.save()

        context = {
            'distance':obj,
            'form': form
        }

        return HttpResponse("ho gya save")
    else:
        form = MeasurementForm()
        context = {
            'form': form
        }
        return render(request,'main.html',context)