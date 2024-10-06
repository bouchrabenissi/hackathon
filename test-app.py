import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

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
        # Paramètres modifiés ici
        "parameters": "T2M,PRECTOT,RH2M,WS2M,ALLSKY_SFC_SW_DWN,TMAX,TMIN,PS,QV10M,SNODP,TS,U10M,U2M,U50M,V10M,V2M,PSC,WD10M,WD2M,WS10M",
        "community": "AG",
        "format": "JSON",
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

# Function to fetch today's weather data from NASA POWER API
def get_current_nasa_data(lat, lon):
    today = datetime.now().strftime("%Y%m%d")  # Get today's date in YYYYMMDD format
    return get_nasa_data(lat, lon, today, today)

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

# Function to train predictive model
def train_predictive_model(df):
    df = df.dropna()  # Remove missing data

    # Check which columns are available in the DataFrame
    required_features = ['PRECTOT', 'RH2M', 'WS2M', 'TMAX', 'TMIN', 'PS', 'QV10M', 'U10M', 'V10M']
    available_features = [feature for feature in required_features if feature in df.columns]

    # Handle case where there are insufficient columns
    if len(available_features) < 2:
        st.error("Not enough features to train the model. Please check the data.")
        return None

    # Define independent (X) and dependent (y) variables
    X = df[available_features]
    y = df['T2M']  # Predict average temperature

    # Split data into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Create and train a random forest model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Predict on the test set
    y_pred = model.predict(X_test)

    # Calculate model evaluation metrics
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    st.write(f"Mean Squared Error: {mse:.2f}")
    st.write(f"R2 Score: {r2:.2f}")

    return model

# Function to generate recommendations based on current data
def generate_recommendations(df, model):
    latest_data = df.iloc[-1]

    # Check if required columns are available for prediction
    required_features = ['PRECTOT', 'RH2M', 'WS2M', 'TMAX', 'TMIN', 'PS', 'QV10M', 'U10M', 'V10M']
    available_features = [feature for feature in required_features if feature in df.columns]

    # Ensure enough features are available to make a prediction
    if len(available_features) < 2:
        st.error("Not enough data available to generate recommendations.")
        return

    # Predict temperature for today using the latest data
    X_latest = latest_data[available_features].values.reshape(1, -1)
    predicted_temp = model.predict(X_latest)[0]

    st.write(f"\nPredicted Temperature: {predicted_temp:.2f}°C")

    if predicted_temp > 30:
        st.write("Drought Alert: High temperature expected, consider increasing irrigation.")
    elif predicted_temp < 0:
        st.write("Frost Alert: Risk of frost expected, take measures to protect crops.")
    else:
        st.write("Optimal climatic conditions for crops.")

# Main Streamlit application
def main():
    st.title("Climate Prediction Tool for Farmers")
    
    # Choose data retrieval method
    data_choice = st.radio("How would you like to obtain the data?", ('API', 'Upload a CSV file'))
    
    if data_choice == 'API':
        # User input: city
        city_name = st.text_input("Enter the name of your city", "Paris")
        
        if st.button("Get data via API"):
            lat, lon = get_lat_lon(city_name)
            
            if lat and lon:
                st.write(f"Coordinates of {city_name}: Latitude = {lat}, Longitude = {lon}")
                
                # Fetch historical data via NASA POWER API
                historical_df = get_nasa_data(lat, lon, "20210101", "20240131")  # Historical date range
                
                if historical_df is not None:
                    # Visualize climatic trends
                    visualize_data(historical_df)
                    
                    # Train predictive model
                    model = train_predictive_model(historical_df)
                    
                    if model:
                        # Fetch current day's data
                        current_df = get_current_nasa_data(lat, lon)
                        
                        if current_df is not None:
                            # Generate recommendations for farmers
                            generate_recommendations(current_df, model)
    
    elif data_choice == 'Upload a CSV file':
        uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])
        
        if uploaded_file is not None:
            # Load data from the uploaded CSV file
            df = pd.read_csv(uploaded_file)
            
            # Convert 'Date' column to datetime if it exists
            if 'Date' in df.columns:
                df['Date'] = pd.to_datetime(df['Date'])
                
            # Check columns
            expected_columns = ['Date', 'T2M', 'PRECTOT', 'RH2M', 'WS2M', 'TMAX', 'TMIN', 'PS', 'QV10M', 'U10M', 'V10M']
            for col in expected_columns:
                if col not in df.columns:
                    st.error(f"The column {col} is missing from the data.")
                    return
            
            # Visualize data
            visualize_data(df)
            
            # Train predictive model
            model = train_predictive_model(df)
            
            if model:
                generate_recommendations(df, model)

if __name__ == "__main__":
    main()
