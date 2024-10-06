from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel
import requests
import pandas as pd
from datetime import datetime, timedelta
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import os
from typing import List, Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = FastAPI(docs_url="/api/py/docs", openapi_url="/api/py/openapi.json")

# NASA POWER API Endpoint
NASA_POWER_URL = "https://power.larc.nasa.gov/api/temporal/daily/point"

# API Key for OpenCage (you need to sign up to get your own key)
OPEN_CAGE_API_KEY = os.getenv('OPEN_CAGE_API_KEY')
if OPEN_CAGE_API_KEY is None:
    print("Warning: OPEN_CAGE_API_KEY environment variable is not set")
    # You could set a default behavior here, or continue with reduced functionality


class CityInput(BaseModel):
    city_name: str
    start_date: str
    end_date: str


class PredictionInput(BaseModel):
    data: List[dict]


class UserInput(BaseModel):
    name: str
    location: str


class LocationInput(BaseModel):
    location: str


@app.get("/api/py/")
def hello_fast_api():
    print("GET /api/py/ endpoint hit")
    return {"message": "Hello from FastAPI"}


@app.post("/api/py/get_lat_lon")
async def get_lat_lon(location: LocationInput):
    if OPEN_CAGE_API_KEY is None:
        raise HTTPException(status_code=500, detail="OpenCage API key is not configured")
    print(
        f"POST /api/py/get_lat_lon endpoint hit with location: {location.location}")
    url = f"https://api.opencagedata.com/geocode/v1/json?q={
        location.location}&key={OPEN_CAGE_API_KEY}"
    response = requests.get(url)
    data = response.json()
    if data['results']:
        result = {
            "lat": data['results'][0]['geometry']['lat'],
            "lon": data['results'][0]['geometry']['lng']
        }
        print(f"Returning lat/lon: {result}")
        return result
    else:
        print(f"Location not found for: {location.location}")
        raise HTTPException(status_code=404, detail="Location not found")


@app.post("/api/py/get_nasa_data")
def get_nasa_data(city_input: CityInput):
    print(f"POST /api/py/get_nasa_data endpoint hit with input: {city_input}")
    lat_lon = get_lat_lon(LocationInput(location=city_input.city_name))
    params = {
        "start": city_input.start_date,
        "end": city_input.end_date,
        "latitude": lat_lon["lat"],
        "longitude": lat_lon["lon"],
        "parameters": "T2M,PRECTOTCORR,RH2M,WS2M,ALLSKY_SFC_SW_DWN,T2M_MAX,T2M_MIN,PS,QV10M,SNODP,TS,U10M,U2M,U50M,V10M,V2M,PSC,WD10M,WD2M,WS10M",
        "community": "AG",
        "format": "JSON",
        "site-elevation": "35"
    }
    print(f"Requesting NASA data with params: {params}")
    response = requests.get(NASA_POWER_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        print("NASA data retrieved successfully")
        return pd.DataFrame(data['properties']['parameter']).to_dict(orient="records")
    else:
        print(f"Error fetching NASA data: {response.status_code}")
        raise HTTPException(status_code=response.status_code,
                            detail=f"Error fetching data from NASA: {response.status_code}")


@app.post("/api/py/train_model")
def train_model(data: List[dict]):
    print(
        f"POST /api/py/train_model endpoint hit with {len(data)} data points")
    df = pd.DataFrame(data)
    df = df.dropna()
    required_features = ['PRECTOTCORR', 'RH2M', 'WS2M', 'T2M_MAX',
                         'T2M_MIN', 'PS', 'QV10M', 'U10M', 'V10M', 'ALLSKY_SFC_SW_DWN']
    available_features = [
        feature for feature in required_features if feature in df.columns]
    if len(available_features) < 2:
        print("Not enough features to train the model")
        raise HTTPException(
            status_code=400, detail="Not enough features to train the model")
    X = df[available_features]
    threshold_temp = 20
    y = (df['T2M'] >= threshold_temp).astype(int)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42)
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)
    print(f"Model trained with accuracy: {accuracy}")
    return {
        "feature_importances": dict(zip(available_features, model.feature_importances_.tolist())),
        "model": model,
        "accuracy": accuracy,
        "classification_report": report
    }


@app.post("/api/py/generate_recommendations")
def generate_recommendations(prediction_input: PredictionInput):
    print(f"POST /api/py/generate_recommendations endpoint hit with {
          len(prediction_input.data)} data points")
    df = pd.DataFrame(prediction_input.data)
    model_result = train_model(prediction_input.data)
    model = model_result["model"]
    latest_data = df.iloc[-1]
    required_features = ['PRECTOTCORR', 'RH2M', 'WS2M', 'T2M_MAX',
                         'T2M_MIN', 'PS', 'QV10M', 'U10M', 'V10M', 'ALLSKY_SFC_SW_DWN']
    available_features = [
        feature for feature in required_features if feature in df.columns]
    if len(available_features) < 2:
        print("Not enough features to generate recommendations")
        raise HTTPException(
            status_code=400, detail="Not enough features to generate recommendations")
    X_latest = latest_data[available_features].values.reshape(1, -1)
    predicted_condition = model.predict(X_latest)[0]
    recommendations = []
    if predicted_condition == 0:
        recommendations = [
            wind_speed_recommendations(latest_data['WS2M'] * 3.6),
            humidity_recommendations(latest_data['RH2M']),
            solar_radiation_recommendations(latest_data['ALLSKY_SFC_SW_DWN']),
            precipitation_recommendations(latest_data['PRECTOTCORR']),
            temperature_recommendations(latest_data['T2M_MAX'])
        ]
    print(f"Generated recommendations: {recommendations}")
    return {
        "predicted_condition": "favorable" if predicted_condition == 1 else "unfavorable",
        "recommendations": recommendations,
        "feature_importances": model_result["feature_importances"],
        "model_accuracy": model_result["accuracy"],
        "classification_report": model_result["classification_report"]
    }


@app.post("/api/py/")
async def process_user_input(user_input: UserInput = Body(...)):
    print(f"POST /api/py/ endpoint hit with user input: {user_input}")
    try:
        city_input = CityInput(city_name=user_input.location, start_date=(datetime.now(
        ) - timedelta(days=30)).strftime("%Y%m%d"), end_date=datetime.now().strftime("%Y%m%d"))
        lat_lon = get_lat_lon(LocationInput(location=user_input.location))
        nasa_data = get_nasa_data(city_input)
        recommendations = generate_recommendations(
            PredictionInput(data=nasa_data))
        message = f"Hello {user_input.name}! Here are your personalized crop care recommendations for {
            user_input.location}:\n\n"
        if recommendations["predicted_condition"] == "favorable":
            message += "The current conditions are favorable for your crops. "
        else:
            message += "The current conditions may pose some challenges for your crops. "
        message += "Here are some specific recommendations:\n\n"
        for rec in recommendations["recommendations"]:
            message += f"- {rec}\n"
        print(f"Returning recommendations for {
              user_input.name} in {user_input.location}")
        return {"message": message}
    except Exception as e:
        print(f"Error processing user input: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Helper functions for recommendations


def wind_speed_recommendations(wind_speed):
    print(f"Generating wind speed recommendation for {wind_speed} km/h")
    wind_speed = wind_speed * 3.6  # Convert from m/s to km/h
    if 0 <= wind_speed < 50:
        return "Light to moderate wind speed: Monitor for light erosion and protect sensitive crops."
    elif 50 <= wind_speed < 60:
        return "Moderate to strong wind speed: Check for damage and use windbreaks."
    elif 70 <= wind_speed < 90:
        return "Strong wind speed: Expect crop damage. Take immediate action to secure plants."
    elif wind_speed >= 100:
        return "Extreme wind speed: Prepare for significant erosion and evacuate at-risk crops."
    elif 120 <= wind_speed <= 250:
        return "Very extreme: Catastrophic damage possible. Take emergency measures and evacuate."
    else:
        return "Please enter a valid wind speed."


def humidity_recommendations(relative_humidity):
    print(f"Generating humidity recommendation for {relative_humidity}%")
    if relative_humidity == 100:
        return "Extreme humidity: Expect soil saturation and possible flooding. Monitor for soil erosion and root rot."
    elif 80 < relative_humidity < 100:
        return "High humidity: Significant moisture retention may lead to fungal growth. Improve drainage and monitor plants."
    elif 50 <= relative_humidity <= 80:
        return "Moderate humidity: Generally favorable for growth. Maintain regular watering and check soil moisture."
    elif relative_humidity < 50:
        return "Low humidity: Soil moisture may evaporate quickly. Increase irrigation to support crop growth."
    else:
        return "Please enter a valid relative humidity percentage."


def solar_radiation_recommendations(solar_irradiance):
    print(f"Generating solar radiation recommendation for {
          solar_irradiance} W/m^2")
    if solar_irradiance >= 1000:
        return "Extreme radiation: High temperatures expected. Increase irrigation and provide shade."
    elif 900 <= solar_irradiance < 1000:
        return "High radiation: Monitor soil moisture and water crops adequately."
    elif 700 <= solar_irradiance < 900:
        return "Moderate radiation: Suitable for growth. Regularly irrigate and check for heat stress."
    elif solar_irradiance < 700:
        return "Low radiation: Ensure adequate sunlight and consider supplemental lighting."
    else:
        return "Enter a valid solar irradiance value."


def precipitation_recommendations(precipitation_rate):
    print(f"Generating precipitation recommendation for {
          precipitation_rate} mm/hr")
    if precipitation_rate > 2:
        return "Extreme precipitation: Rapid erosion and waterlogging expected. Manage drainage to prevent flooding."
    elif 1 <= precipitation_rate <= 2:
        return "High precipitation: Risk of flash flooding. Monitor drainage and prepare for runoff."
    elif 0.5 <= precipitation_rate < 1:
        return "Moderate precipitation: Monitor soil saturation and prepare for localized flooding."
    elif precipitation_rate < 0.5:
        return "Low precipitation: Favorable for planting. Consider irrigation if moisture drops."
    else:
        return "Enter a valid precipitation rate."


def temperature_recommendations(temperature):
    print(f"Generating temperature recommendation for {temperature}°C")
    if temperature > 70:
        return "Extreme: High risk of land degradation. Increase irrigation and provide shade."
    elif 60 < temperature <= 70:
        return "High: Expect rapid soil drying. Monitor moisture and reduce water loss."
    elif 50 < temperature <= 60:
        return "Very high: Soil may crack. Increase irrigation and consider mulching."
    elif 40 < temperature <= 50:
        return "High: Increased evaporation. Monitor for water stress and adjust watering."
    elif temperature <= 40:
        return "Moderate: Generally manageable for growth. Continue regular irrigation."
    else:
        return "Enter a valid temperature value."


@app.post("/api/py/get_chart_data")
def get_chart_data(city_input: CityInput):
    print(f"POST /api/py/get_chart_data endpoint hit with input: {city_input}")
    nasa_data = get_nasa_data(city_input)
    df = pd.DataFrame(nasa_data)
    df['date'] = pd.to_datetime(df.index)

    temperature_data = process_temperature_data(df)
    precipitation_data = process_precipitation_data(df)
    wind_speed_data = process_wind_speed_data(df)
    solar_radiation_data = process_solar_radiation_data(df)

    return {
        "temperature": temperature_data,
        "precipitation": precipitation_data,
        "windSpeed": wind_speed_data,
        "solarRadiation": solar_radiation_data
    }


def process_temperature_data(df):
    return [
        {
            "date": row['date'].strftime("%Y-%m-%d"),
            "min": row['T2M_MIN'],
            "max": row['T2M_MAX'],
            "avg": row['T2M']
        }
        for _, row in df.iterrows()
    ]


def process_precipitation_data(df):
    return [
        {
            "date": row['date'].strftime("%Y-%m-%d"),
            "value": row['PRECTOTCORR']
        }
        for _, row in df.iterrows()
    ]


def process_wind_speed_data(df):
    return [
        {
            "date": row['date'].strftime("%Y-%m-%d"),
            "value": row['WS2M']
        }
        for _, row in df.iterrows()
    ]


def process_solar_radiation_data(df):
    return [
        {
            "date": row['date'].strftime("%Y-%m-%d"),
            "value": row['ALLSKY_SFC_SW_DWN']
        }
        for _, row in df.iterrows()
    ]