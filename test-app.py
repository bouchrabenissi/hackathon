import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# NASA POWER API Endpoint
NASA_POWER_URL = "https://power.larc.nasa.gov/api/temporal/daily/point"

# API Key for OpenCage (you need to sign up to get your own key)
OPEN_CAGE_API_KEY = 'f2a2c8e0de9147c28956f29a4fbbbc4e'

# Function to get latitude and longitude of a city via OpenCage API
def get_lat_lon(city_name):
    url = f"https://api.opencagedata.com/geocode/v1/json?q={city_name}&key={OPEN_CAGE_API_KEY}"
    response = requests.get(url)
    data = response.json()
    if data['results']:
        return data['results'][0]['geometry']['lat'], data['results'][0]['geometry']['lng']
    else:
        st.error("City not found. Please check the name.")
        return None, None

# Function to fetch historical weather data via NASA POWER API
def get_nasa_data(lat, lon, start_date, end_date):
    params = {
        "start": start_date,
        "end": end_date,
        "latitude": lat,
        "longitude": lon,
        "parameters": "T2M,PRECTOTCORR,RH2M,WS2M,ALLSKY_SFC_SW_DWN,T2M_MAX,T2M_MIN,PS,QV10M,SNODP,TS,U10M,U2M,U50M,V10M,V2M,PSC,WD10M,WD2M,WS10M",
        "community": "AG",
        "format": "JSON",
        "site-elevation": "35"  # Ensure site elevation parameter is included
    }

    response = requests.get(NASA_POWER_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        parameters = data['properties']['parameter']

        # Create a date range based on the provided dates
        dates = pd.date_range(start=start_date, end=end_date, freq='D')
        df = pd.DataFrame(parameters)

        # Insert the Date column at the beginning of the DataFrame
        df.insert(0, 'Date', dates)

        return df
    else:
        st.error(f"Error fetching data from NASA: {response.status_code}")
        return None

# Function to visualize climatic trends
def visualize_data(df):
    plt.figure(figsize=(12, 8))
    
    # Plot average, max, and min temperatures
    plt.subplot(2, 1, 1)
    plt.plot(df['Date'], df['T2M'], label='Temperature (°C)', color='blue')
    
    if 'TMAX' in df.columns:
        plt.plot(df['Date'], df['TMAX'], label='Max Temperature (°C)', color='red')
    
    if 'TMIN' in df.columns:
        plt.plot(df['Date'], df['TMIN'], label='Min Temperature (°C)', color='green')
    
    plt.title('Temperatures (°C)')
    plt.legend()

    if 'PRECTOT' in df.columns:
        plt.subplot(2, 1, 2)
        plt.bar(df['Date'], df['PRECTOT'], label='Precipitation (mm)', color='orange', alpha=0.5)
        plt.title('Precipitation (mm)')
        plt.legend()
    
    st.pyplot(plt)

# Function to train predictive model for classification
def train_classification_model(df):
    df = df.dropna()  # Remove missing data

    # Check which columns are available in the DataFrame
    required_features = ['PRECTOTCORR', 'RH2M', 'WS2M', 'T2M_MAX', 'T2M_MIN', 'PS', 'QV10M', 'U10M', 'V10M', 'ALLSKY_SFC_SW_DWN']
    available_features = [feature for feature in required_features if feature in df.columns]

    # Handle case where there are insufficient columns
    if len(available_features) < 2:
        st.error("Not enough features to train the model. Please check the data.")
        return None

    # Define independent (X) and dependent (y) variables
    X = df[available_features]
    # Create a binary classification target variable based on temperature
    # Define a threshold temperature, for example, 20°C
    threshold_temp = 20  
    y = (df['T2M'] >= threshold_temp).astype(int)  # 1 for favorable, 0 for unfavorable

    # Split data into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Create and train a random forest classifier
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Predict on the test set
    y_pred = model.predict(X_test)

    # Calculate model evaluation metrics
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)

    st.write(f"Accuracy: {accuracy:.2f}")
    st.write("Classification Report:")
    st.text(report)

    return model

def wind_speed_recommendations(wind_speed):
    wind_speed = wind_speed * 3.6  # Convert from m/s to km/h
    if 0 <= wind_speed < 50:
        return ("Light to moderate wind speed: Monitor for light erosion and protect sensitive crops.")
    
    elif 50 <= wind_speed < 60:
        return ("Moderate to strong wind speed: Check for damage and use windbreaks.")
    
    elif 70 <= wind_speed < 90:
        return ("Strong wind speed: Expect crop damage. Take immediate action to secure plants.")
    
    elif wind_speed >= 100:
        return ("Extreme wind speed: Prepare for significant erosion and evacuate at-risk crops.")
    
    elif 120 <= wind_speed <= 250:
        return ("Very extreme: Catastrophic damage possible. Take emergency measures and evacuate.")

    else:
        return "Please enter a valid wind speed."

def humidity_recommendations(relative_humidity):
    if relative_humidity == 100:
        return ("Extreme humidity: Expect soil saturation and possible flooding. Monitor for soil erosion and root rot.")
    
    elif 80 < relative_humidity < 100:
        return ("High humidity: Significant moisture retention may lead to fungal growth. Improve drainage and monitor plants.")
    
    elif 50 <= relative_humidity <= 80:
        return ("Moderate humidity: Generally favorable for growth. Maintain regular watering and check soil moisture.")
    
    elif relative_humidity < 50:
        return ("Low humidity: Soil moisture may evaporate quickly. Increase irrigation to support crop growth.")
    
    else:
        return "Please enter a valid relative humidity percentage."


def solar_radiation_recommendations(solar_irradiance):
    if solar_irradiance >= 1000:
        return ("Extreme radiation: High temperatures expected. Increase irrigation and provide shade.")

    elif 900 <= solar_irradiance < 1000:
        return ("High radiation: Monitor soil moisture and water crops adequately.")

    elif 700 <= solar_irradiance < 900:
        return ("Moderate radiation: Suitable for growth. Regularly irrigate and check for heat stress.")

    elif solar_irradiance < 700:
        return ("Low radiation: Ensure adequate sunlight and consider supplemental lighting.")

    else:
        return "Enter a valid solar irradiance value."


def precipitation_recommendations(precipitation_rate):
    if precipitation_rate > 2:
        return ("Extreme precipitation: Rapid erosion and waterlogging expected. Manage drainage to prevent flooding.")

    elif 1 <= precipitation_rate <= 2:
        return ("High precipitation: Risk of flash flooding. Monitor drainage and prepare for runoff.")

    elif 0.5 <= precipitation_rate < 1:
        return ("Moderate precipitation: Monitor soil saturation and prepare for localized flooding.")

    elif precipitation_rate < 0.5:
        return ("Low precipitation: Favorable for planting. Consider irrigation if moisture drops.")

    else:
        return "Enter a valid precipitation rate."

def temperature_recommendations(temperature):
    if temperature > 70:
        return ("Extreme: High risk of land degradation. Increase irrigation and provide shade.")

    elif 60 < temperature <= 70:
        return ("High: Expect rapid soil drying. Monitor moisture and reduce water loss.")

    elif 50 < temperature <= 60:
        return ("Very high: Soil may crack. Increase irrigation and consider mulching.")

    elif 40 < temperature <= 50:
        return ("High: Increased evaporation. Monitor for water stress and adjust watering.")

    elif temperature <= 40:
        return ("Moderate: Generally manageable for growth. Continue regular irrigation.")

    else:
        return "Enter a valid temperature value."

# Function to generate recommendations based on current data
def generate_recommendations(df, model):
    latest_data = df.iloc[-1]

    # Check if required columns are available for prediction
    required_features = ['PRECTOTCORR', 'RH2M', 'WS2M', 'T2M_MAX', 'T2M_MIN', 'PS', 'QV10M', 'U10M', 'V10M', 'ALLSKY_SFC_SW_DWN']
    available_features = [feature for feature in required_features if feature in df.columns]
    
    # Ensure enough features are available to make a prediction
    if len(available_features) < 2:
        st.error("Not enough features to generate recommendations.")
        return None

    # Predict agronomic condition using the latest data
    X_latest = latest_data[available_features].values.reshape(1, -1)
    predicted_condition = model.predict(X_latest)[0]

    if predicted_condition == 1:
        st.success("Agronomic conditions are favorable.")
    else:
        st.warning("Agronomic conditions are unfavorable.")
        st.write("Recommendations:")
        
        # Call recommendation functions
        wind_speed_recommendation = wind_speed_recommendations(latest_data['WS2M'] * 3.6)  # Convert to km/h
        humidity_recommendation = humidity_recommendations(latest_data['RH2M'])
        solar_radiation_recommendation = solar_radiation_recommendations(latest_data['ALLSKY_SFC_SW_DWN'])
        precipitation_recommendation = precipitation_recommendations(latest_data['PRECTOTCORR'])
        temperature_recommendation = temperature_recommendations(latest_data['T2M_MAX'])  # Use TMAX for temperature

        # Display all recommendations
        st.write(f"- {wind_speed_recommendation}")
        st.write(f"- {humidity_recommendation}")
        st.write(f"- {solar_radiation_recommendation}")
        st.write(f"- {precipitation_recommendation}")
        st.write(f"- {temperature_recommendation}")

    # Identify key factors contributing to favorable conditions (if favorable)
    if predicted_condition == 1:
        st.write("Factors contributing to favorable conditions:")
        feature_importances = model.feature_importances_
        feature_names = available_features
        sorted_indices = feature_importances.argsort()[::-1]
        for i in sorted_indices:
            st.write(f"{feature_names[i]}: {feature_importances[i]:.4f}")

# Main Streamlit application
def main():
    st.title("Climate Prediction Tool for Farmers")
    
    # Choose data retrieval method
    data_choice = st.radio("How would you like to obtain the data?", ('API', 'Upload a CSV file'))
    
    if data_choice == 'API':
        # User input: city
        city_name = st.text_input("Enter the name of your city", "Paris")
        
        # Date selection
        start_date = st.date_input("Select Start Date", datetime(2020, 1, 1))
        end_date = st.date_input("Select End Date", datetime(2024, 1, 31))
        
        if st.button("Get data via API"):
            lat, lon = get_lat_lon(city_name)
            
            if lat and lon:
                historical_df = get_nasa_data(lat, lon, start_date.strftime("%Y%m%d"), end_date.strftime("%Y%m%d"))
                
                if historical_df is not None:
                    st.write("Historical Weather Data:")
                    st.dataframe(historical_df)
                    
                    visualize_data(historical_df)
                    
                    model = train_classification_model(historical_df)
                    if model:
                        generate_recommendations(historical_df, model)

    else:
        uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])
        if uploaded_file is not None:
            historical_df = pd.read_csv(uploaded_file)
            st.write("Historical Weather Data:")
            st.dataframe(historical_df)
            
            visualize_data(historical_df)
            
            model = train_classification_model(historical_df)
            if model:
                generate_recommendations(historical_df, model)

if __name__ == "__main__":
    main()
