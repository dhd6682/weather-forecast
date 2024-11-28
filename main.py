from fastapi import FastAPI, HTTPException
import requests
from datetime import datetime, timedelta
from fastapi.responses import JSONResponse
import os

app = FastAPI()

def get_weather_data(api_key, city):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&units=metric&appid={api_key}" # 기상청 날씨 api 가져오기
    try:
        response = requests.get(url)
        response.raise_for_status()  # HTTP 에러 발생 시 예외 처리
    except requests.exceptions.HTTPError as http_err:
        raise HTTPException(status_code=response.status_code, detail=f"HTTP error occurred: {http_err}")
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"An error occurred: {err}")
    
    return response.json()

def parse_weather(data):
    # API 응답에서 'list' 키가 존재하는지 확인
    if 'list' not in data:
        raise HTTPException(status_code=500, detail="Invalid response format from weather API")
    
    # 오늘 날짜
    today = datetime.now().date()
    tomorrow = today + timedelta(days=1)

    today_weather = None
    tomorrow_weather = None

    for entry in data['list']:
        date_time = datetime.fromtimestamp(entry['dt'])
        if date_time.date() == today:
            today_weather = entry
        elif date_time.date() == tomorrow:
            tomorrow_weather = entry
            break

    return today_weather, tomorrow_weather

@app.get("/weather/{city}")
def read_weather(city: str):
    api_key = "c26b618c96d7fa98d27a60189767bcbd"  # 여기 API 키를 입력하세요
    data = get_weather_data(api_key, city)
    today_weather, tomorrow_weather = parse_weather(data)

    if not today_weather or not tomorrow_weather:
        raise HTTPException(status_code=404, detail="Weather data not found")

    return JSONResponse({
        "today": {
            "temperature": today_weather['main']['temp'],
            "weather": today_weather['weather'][0]['main'],
            "humidity": today_weather['main']['humidity'],
            "wind_speed": today_weather['wind']['speed']
        },
        "tomorrow": {
            "temperature": tomorrow_weather['main']['temp'],
            "weather": tomorrow_weather['weather'][0]['main'],
            "humidity": tomorrow_weather['main']['humidity'],
            "wind_speed": tomorrow_weather['wind']['speed']
        }
    })

@app.post("/weather/{city}")
def read_weather(city: str):
    api_key = os.getenv("API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="API key not found")  # 여기 API 키를 입력하세요
    data = get_weather_data(api_key, city)
    today_weather, tomorrow_weather = parse_weather(data)

    if not today_weather or not tomorrow_weather:
        raise HTTPException(status_code=404, detail="Weather data not found")

    return JSONResponse({
        "today": {
            "temperature": today_weather['main']['temp'],
            "weather": today_weather['weather'][0]['description'],
            "humidity": today_weather['main']['humidity'],
            "wind_speed": today_weather['wind']['speed']
        },
        "tomorrow": {
            "temperature": tomorrow_weather['main']['temp'],
            "weather": tomorrow_weather['weather'][0]['description'],
            "humidity": tomorrow_weather['main']['humidity'],
            "wind_speed": tomorrow_weather['wind']['speed']
        }
    })