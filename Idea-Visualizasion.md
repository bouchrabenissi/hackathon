# Précipitations:

- __Type de graphe__: bar chart 
- __Input__: PRECTOTCORR (Précipitations Totales), date
- __Output__: Graphique à barres montrant le nombre de précipitation (PRECTOT > 0) 
- __Description__: Cette visualisation montre la fréquence des jours de pluie 
- _Chart title_: "Total Precipitation Frequency"
  _X-axis_: "Date" (or "Days" if you're showing a range of days)
  _Y-axis_: "Number of Precipitation Days" (or simply "Precipitation Amount (mm)" if you prefer to show the actual precipitation values)
____________________________________________________________________________
# Tempétature:

- __Input__: T2M (Température à 2 mètres)
- __Output__: Jauge représentant la température moyenne dans une plage définie (par exemple, entre 0°C et 40°C).
- __Description__: La jauge indique visuellement si la température est faible, modérée ou élevée, selon une plage définie. C'est utile pour voir rapidement si la température actuelle est dans une zone critique pour les cultures.
- _Chart title_: "Average Temperature Gauge"
_X-axis_: This chart typically doesn't require an x-axis as it is a gauge; instead, you might label the sections directly on the gauge itself (e.g., "Low," "Moderate," "High").
_Y-axis_: Similarly, a traditional y-axis is not necessary for a gauge chart. However, you can annotate temperature ranges (e.g., "0°C to 40°C") along the gauge.

____________________________________________________________________________
# Humidité:
	
- __Type de graphe__: Line chart
- __Input__: RH2M (Humidité relative à 2 mètres), date
- __Output__: Un graphique linéaire montrant l’évolution de l’humidité relative au fil du temps.
- __Description__: Cette visualisation permet de suivre comment l'humidité relative change dans une période donnée. Une humidité élevée indique souvent des conditions favorables pour la culture, tandis qu'une humidité trop basse peut être un signe de sécheresse.
- _Chart title_: "Relative Humidity Over Time"
_X-axis (horizontal)_: "Date"
_Y-axis (vertical)_: "Relative Humidity (%)
____________________________________________________________________________
# All together:

- __Type de graphe__: Radar Chart
- __Input__: T2M, WS2M, RH2M, PRECTOT, ALLSKY_SFC_SW_DWN
- __Output__: Radar Chart
- __Description__: This radar chart gives farmers a clear view of weather conditions, helping with decisions on planting, irrigation, and crop protection. It visualizes key factors like temperature, wind speed, humidity, precipitation, and solar radiation, making it easy to assess if the weather is favorable or if adjustments are needed. 
- _Chart title_: Weather Conditions Overview for Farmers
_The name of the parameters_:
T2M: Temperature
WS2M: Wind Speed
RH2M: Humidity
PRECTOTCORR: Precipitation
ALLSKY_SFC_SW_DWN: Solar Radiation
