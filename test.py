import requests
from datetime import datetime, timedelta
import math
from fastapi import FastAPI

app=FastAPI()
def fetch_sun_data(latitude, longitude):
    url = 'https://api.sunrise-sunset.org/json'
    start_date = datetime(2022, 1, 1)
    end_date = datetime(2022, 12, 31)
    current_date = start_date
    sun_data = []

    while current_date <= end_date:
        formatted_date = current_date.strftime('%Y-%m-%d')
        params = {'lat': latitude, 'lng': longitude, 'date': formatted_date}
        response = requests.get(url=url, params=params)
        data = response.json().get('results')

        if data:
            data['date'] = formatted_date
            sun_data.append(data)

        current_date += timedelta(days=30)

    return sun_data



# Convert day lengths to seconds for easier averaging
def time_to_seconds(time_str):
    hours, minutes, seconds = map(int, time_str.split(':'))
    total_seconds = hours * 3600 + minutes * 60 + seconds
    return total_seconds


def calculate_average(sun_data):
  day_lengths = [d['day_length'] for d in sun_data]
  day_lengths_seconds = [time_to_seconds(dl) for dl in day_lengths]
  average_day_length_seconds = sum(day_lengths_seconds) / len(day_lengths_seconds)
  print(average_day_length_seconds)
  return average_day_length_seconds


@app.get("/calculate_percentage/")
async def calculate_percentage(latitude: float, longitude: float):
    sun_data = fetch_sun_data(50, 70)
    average_day_seconds = calculate_average(sun_data)
    k = 0.12 # Adjust this value as needed
    average_day_second = 40000  # Adjust this value as needed

    percentage = 100 * (1 - math.exp(-k * (average_day_second / 3600)))

    print(percentage)
    return {"latitude": latitude, "longitude": longitude, "percentage": percentage}