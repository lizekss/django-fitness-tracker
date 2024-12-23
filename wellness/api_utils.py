import os

import requests
from django.core.cache import cache
from dotenv import load_dotenv

load_dotenv()


def get_available_activities_example():
    return ['Yoga',
            'Running, 5 mph (12 minute mile)',
            'Cycling, <10 mph, leisure bicycling',
            'Swimming',
            'Rock Climbing',
            'Walking the dog',
            'Soccer',
            'Badminton',
            'Baseball',
            'Basketball',
            'Frisbee',
            'Golf',
            'Boxing',
            'Tennis',
            'Boxing',
            'Hockey',
            'Tai Chi',
            'Football',
            'Ping pong',
            'Ice skating',
            'Rollerblading',
            'Kayaking',
            ]


def get_available_activities():
    api_key = os.getenv('APININJAS_API_KEY')
    url = "https://api.api-ninjas.com/v1/caloriesburnedactivities"

    headers = {
        'X-Api-Key': api_key
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        return [activity['name'] for activity in data]
    except requests.exceptions.RequestException as e:
        print(f"Error fetching activities: {e}")
        return []


def get_calories_burned(activity_type, duration_minutes, weight):
    cache_key = f"activity_calories_per_hour_{activity_type}_{weight}"

    # Try to get the calories per hour value from the cache
    calories_per_hour = cache.get(cache_key)

    if calories_per_hour:
        return calories_per_hour * duration_minutes / 60
    else:
        api_key = os.getenv('APININJAS_API_KEY')
        url = f"https://api.api-ninjas.com/v1/caloriesburned?activity={activity_type}&duration={duration_minutes}"
        if weight:
            weight_lbs = int(weight * 2.20462)
            url += f"&weight={weight_lbs}"
        headers = {
            'X-Api-Key': api_key
        }

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()[0]
            cache.set(cache_key, data.get('calories_per_hour', 0))
            return data.get('total_calories', 0)
        except requests.exceptions.RequestException as e:
            print(f"Error calling API: {e}")
            return 0


def get_meal_calories(description):
    api_key = os.getenv('CALORIENINJAS_API_KEY')
    api_url = 'https://api.calorieninjas.com/v1/nutrition?query='
    query = description
    response = requests.get(api_url + query, headers={'X-Api-Key': api_key})

    if response.status_code == 200:
        data = response.json()
        if 'items' in data:
            return sum([item.get('calories', 0) for item in data['items']])
        else:
            return 0
    else:
        print(f"Error fetching data from API: {response.status_code}")
        return 0
