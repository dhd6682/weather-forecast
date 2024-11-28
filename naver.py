from fastapi import FastAPI, HTTPException
import requests
from bs4 import BeautifulSoup

app = FastAPI()

NAVER_WEATHER_URL = "https://search.naver.com/search.naver?query={} 날씨"

def get_weather(city_name: str):
    # 네이버 날씨 페이지 요청
    url = NAVER_WEATHER_URL.format(city_name)
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        try:
            # 오늘 날씨 정보 추출
            temperature = soup.find('div', class_='temperature_text').text.strip()
            weather_desc = soup.find('p', class_='summary').text.strip()

            # 내일 날씨 정보 추출 (span class="menu"에서 찾기)
            tomorrow_menu_element = soup.find('span', class_='menu')
            if not tomorrow_menu_element:
                raise HTTPException(status_code=404, detail="Tomorrow's weather information not found")

            # 내일 날씨 정보는 클릭할 수 있는 요소 내부에 있음
            tomorrow_temp_element = tomorrow_menu_element.find_next('span', class_='temperature_text')
            tomorrow_weather_element = tomorrow_menu_element.find_next('span', class_='summary')

            if tomorrow_temp_element and tomorrow_weather_element:
                tomorrow_temp = tomorrow_temp_element.text.strip()
                tomorrow_weather_desc = tomorrow_weather_element.text.strip()
            else:
                raise HTTPException(status_code=404, detail="Tomorrow's weather information not found")
            
            return {
                "city": city_name,
                "today": {
                    "temperature": temperature,
                    "description": weather_desc
                },
                "tomorrow": {
                    "temperature": tomorrow_temp,
                    "description": tomorrow_weather_desc
                }
            }
        except AttributeError:
            raise HTTPException(status_code=404, detail="Weather information not found")
    else:
        raise HTTPException(status_code=response.status_code, detail="Failed to retrieve weather data")

@app.get("/weather/{city_name}")
def read_weather(city_name: str):
    return get_weather(city_name)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
