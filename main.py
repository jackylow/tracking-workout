import requests
from datetime import datetime
import os

APP_ID = os.environ.get("ON_APP_ID")
API_KEY = os.environ.get("ON_API_KEY")
NAME = os.environ.get("ON_NAME")
PASSWORD = os.environ.get("ON_PASSWORD")
AUTH = (NAME, PASSWORD)

today = datetime.now()

headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
}

exercise_endpoints = "https://trackapi.nutritionix.com/v2/natural/exercise"

exercise_param = {
    "query": input("Which exercises you did: "),
    "gender": "female",
    "weight_kg": 120,
    "height_cm": 180,
    "age": 45,
}

response = requests.post(url=exercise_endpoints, json=exercise_param, headers=headers)
result = response.json()

sheet_endpoint = os.environ.get("SHEET_ENDPOINT")

# оформляем таблицу в google sheets
for exercise in result["exercises"]:
    sheet_param = {
        "workout": {
            "date": today.strftime("%d/%m/%Y"),
            "time": today.strftime("%H:%M:%S"),
            "exercise": exercise["user_input"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]
        }
    }

    res = requests.post(url=sheet_endpoint, json=sheet_param, auth=AUTH)
    print(res.text)
