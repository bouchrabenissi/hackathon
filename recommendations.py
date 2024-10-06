def wind_speed_recommendations(wind_speed):
    wind_speed = wind_speed * 3.6  # Convert from m/s to km/h
    if 30 <= wind_speed < 50:
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
