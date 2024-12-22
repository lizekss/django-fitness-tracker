import os

import requests
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


def get_calories_burned(activity_type, duration_minutes):
    api_key = os.getenv('APININJAS_API_KEY')
    url = f"https://api.api-ninjas.com/v1/caloriesburned?activity={activity_type}&duration={duration_minutes}"

    headers = {
        'X-Api-Key': api_key
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()[0]
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
