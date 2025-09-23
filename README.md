# Weather Forecast AI API 🌦️

이 프로젝트는 특정 도시의 오늘과 내일의 날씨를 예측하는 AI 기반 웹 API입니다. FastAPI와 OpenWeatherMap API를 사용하여 날씨 데이터를 수집하고, 사용자가 날씨 정보를 조회할 수 있도록 합니다. 이 `README.md` 파일은 프로젝트의 주요 AI 기능을 중심으로 설명합니다.

## 목차
1. [코드 소개](#코드-소개)
2. [주요 기능](#주요-기능)
3. [설치 및 사용 방법](#설치-및-사용-방법)
4. [API 설명](#api-설명)
5. [환경 변수 설정](#환경-변수-설정)
6. [기여 방법](#기여-방법)
7. [라이센스](#라이센스)

## 코드 소개

Weather Forecast AI API는 도시 이름을 입력받아 해당 도시의 오늘과 내일의 날씨를 예측하는 기능을 제공합니다. 이 프로젝트는 **FastAPI**와 **OpenWeatherMap API**를 활용하여 기상 데이터를 처리하며, 사용자에게 직관적인 REST API 형식으로 결과를 제공합니다. 이 프로젝트는 AI 기반 데이터 분석과 예측을 중심으로 구축되어 있으며, 날씨 데이터 처리와 예측을 효율적으로 수행합니다.

## 주요 기능

### 1. 날씨 데이터 수집 및 예외 처리
- **OpenWeatherMap API**를 통해 실시간 날씨 예보 데이터를 수집합니다.
- HTTP 요청을 통해 날씨 데이터를 가져오며, 다양한 오류에 대한 예외 처리를 수행합니다 (예: HTTP 오류, 네트워크 오류 등).

### 2. 데이터 파싱 및 예측
- 수집된 날씨 데이터를 **Python의 datetime** 모듈을 사용해 오늘과 내일로 구분합니다.
- 오늘과 내일의 날씨 정보를 파싱하여 온도, 습도, 풍속 등의 정보를 추출하고, 사용자 요청에 따라 반환합니다.

### 3. REST API 구현
- **GET** 및 **POST** 요청을 처리하는 API 엔드포인트를 제공합니다.
- 사용자는 `/weather/{city}` 엔드포인트를 통해 도시의 날씨를 조회할 수 있습니다.

## 설치 및 사용 방법

### 요구 사항
- Python 3.8+
- FastAPI
- requests
- uvicorn
- python-dotenv

### 설치 방법

1. **프로젝트 클론**:
   ```bash
   git clone https://github.com/dhd6682/weather-forecast.git
   cd weather-forecast
   ```

2. **필요한 라이브러리 설치**:
   ```bash
   pip install -r requirements.txt
   ```

3. **환경 변수 설정**:
   프로젝트 루트에 `.env` 파일을 생성하고 다음과 같이 API 키를 설정합니다:
   ```
   API_KEY=your_openweathermap_api_key
   ```
   
   **중요**: `.env` 파일은 Git에 업로드되지 않습니다. 각자 OpenWeatherMap에서 API 키를 발급받아 설정해야 합니다.

4. **서버 실행**:
   ```bash
   uvicorn main:app --reload
   ```

5. **API 사용**:
   브라우저 또는 API 클라이언트를 사용해 다음 URL로 접근할 수 있습니다:
   ```
   http://127.0.0.1:8000/weather/{city}
   ```
   여기서 `{city}`는 날씨를 조회할 도시의 이름입니다 (예: `seoul`).

## API 설명

### 1. GET /weather/{city}
- **설명**: 입력된 도시의 오늘과 내일의 날씨 정보를 반환합니다.
- **요청**: 도시 이름 (`city`)을 URL에 포함시켜 GET 요청을 보냅니다.
- **응답 예시**:
  ```json
  {
    "today": {
      "temperature": 22.5,
      "weather": "Clear",
      "humidity": 60,
      "wind_speed": 5.2
    },
    "tomorrow": {
      "temperature": 23.4,
      "weather": "Clouds",
      "humidity": 55,
      "wind_speed": 4.8
    }
  }
  ```

### 2. POST /weather/{city}
- **설명**: POST 요청을 통해 날씨 정보를 조회하며, 추가적인 설정이나 파라미터를 전달할 수 있습니다.
- **응답 예시**: GET 요청과 동일한 구조로 오늘과 내일의 날씨 정보를 반환합니다.

## 환경 변수 설정

이 프로젝트에서는 OpenWeatherMap API 키와 같은 중요한 정보를 `.env` 파일을 통해 관리합니다. API 키와 같은 민감한 정보가 GitHub에 노출되지 않도록 보호해줍니다.

### .env 파일 예시
```
API_KEY=your_openweathermap_api_key
```


