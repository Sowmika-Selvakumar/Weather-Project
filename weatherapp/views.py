from django.shortcuts import render
from django.contrib import messages
import requests
import datetime

def home(request):
    city = request.POST.get('city', 'Chennai')  # default city

    # Weather API
    weather_url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid=8eca1697ba7752bd391eb843a53d68a1'
    PARAMS = {'units': 'metric'}

    # Unsplash API for dynamic city images
    UNSPLASH_ACCESS_KEY = 'IcdYVRVHjp87XEC0n5jnqbPy6qeOS6jzqp3zZPz5kyI'
    unsplash_url = f'https://api.unsplash.com/photos/random?query={city}&orientation=landscape&client_id={UNSPLASH_ACCESS_KEY}'

    try:
        # Get city image
        img_data = requests.get(unsplash_url).json()
        image_url = img_data.get('urls', {}).get('regular', 'https://images.pexels.com/photos/3008509/pexels-photo-3008509.jpeg?auto=compress&cs=tinysrgb&w=1600')

        # Get weather data
        weather_data = requests.get(weather_url, params=PARAMS).json()
        description = weather_data['weather'][0]['description']
        icon = weather_data['weather'][0]['icon']
        temp = weather_data['main']['temp']
        day = datetime.date.today()

        return render(request, 'weatherapp/home.html', {
            'description': description,
            'icon': icon,
            'temp': temp,
            'day': day,
            'city': city,
            'exception_occurred': False,
            'image_url': image_url
        })

    except:
        messages.error(request, 'City information is not available.')
        day = datetime.date.today()
        return render(request, 'weatherapp/home.html', {
            'description': 'clear sky',
            'icon': '01d',
            'temp': 25,
            'day': day,
            'city': 'Chennai',
            'exception_occurred': True,
            'image_url': 'https://images.pexels.com/photos/3008509/pexels-photo-3008509.jpeg?auto=compress&cs=tinysrgb&w=1600'
        })
