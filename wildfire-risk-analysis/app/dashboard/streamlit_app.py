import streamlit as st
import pandas as pd
import joblib
import geopandas as gpd
from datetime import datetime, timezone
import requests
import os
from dotenv import load_dotenv
from shapely.geometry import Point
from streamlit_folium import st_folium
import folium

# Load environment variables
load_dotenv()
OWM_API_KEY = os.getenv("OWM_API_KEY")

# Load model artifacts
model = joblib.load("wildfire-risk-analysis/models/fire_risk_classifier.pkl")
scaler = joblib.load("wildfire-risk-analysis/models/feature_scaler.pkl")
feature_cols = joblib.load("wildfire-risk-analysis/models/feature_list.pkl")
label_encoder = joblib.load("wildfire-risk-analysis/models/label_encoder.pkl")

# Load FIRMS shapefile
FIRMS_FILE = "/home/saiteja/Wildfire-Risk-Analysis-System/wildfire-risk-analysis/notebooks/data/processed/raw/MODIS_C6_1_USA_contiguous_and_Hawaii_24h.shp"

gdf_firms = gpd.read_file(FIRMS_FILE).to_crs(epsg=4326)

def get_weather(lat, lon):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OWM_API_KEY}&units=metric"
    res = requests.get(url)
    if res.status_code != 200:
        return None
    data = res.json()
    return {
        "temperature": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "wind_speed": data["wind"]["speed"],
        "weather_main": data["weather"][0]["main"],
        "timestamp": data["dt"]
    }

def get_nearest_fire_data(lat, lon, radius_km=50):
    user_point = gpd.GeoSeries([Point(lon, lat)], crs="EPSG:4326").to_crs(epsg=3857)
    gdf_buffer = user_point.buffer(radius_km * 1000).to_crs(epsg=4326)
    gdf_nearby = gdf_firms[gdf_firms.to_crs(epsg=4326).intersects(gdf_buffer[0])]
    if gdf_nearby.empty:
        return None
    nearest = gdf_nearby.iloc[0]
    return {
        "brightness": nearest["BRIGHTNESS"],
        "frp": nearest["FRP"]
    }

def predict_fire_risk_verbose(lat, lon, brightness, frp):
    weather = get_weather(lat, lon)
    if not weather:
        return None

    wind_factor = brightness * weather["wind_speed"]
    is_daytime = 1 if 6 <= datetime.fromtimestamp(weather["timestamp"], tz=timezone.utc).hour <= 18 else 0

    weather_conditions = ["Clear", "Clouds", "Rain", "Haze"]
    weather_ohe = {f"weather_{w}": 1 if weather["weather_main"] == w else 0 for w in weather_conditions}
    for col in [c for c in feature_cols if c.startswith("weather_")]:
        weather_ohe.setdefault(col, 0)

    input_data = {
        "brightness": brightness,
        "frp": frp,
        "temperature": weather["temperature"],
        "humidity": weather["humidity"],
        "wind_speed": weather["wind_speed"],
        "wind_factor": wind_factor,
        "is_daytime": is_daytime,
        **weather_ohe
    }

    df_input = pd.DataFrame([input_data])[feature_cols]
    df_scaled = scaler.transform(df_input)

    pred = model.predict(df_scaled)[0]
    prob = model.predict_proba(df_scaled)[0]
    risk_label = label_encoder.inverse_transform([pred])[0]
    confidence = round(prob[pred] * 100, 2)

    return {
        "Fire Risk": risk_label,
        "Confidence": f"{confidence}%",
        "Weather": weather["weather_main"],
        "Temperature": f"{weather['temperature']}\u00b0C",
        "Humidity": f"{weather['humidity']}%",
        "Wind Speed": f"{weather['wind_speed']} m/s",
        "Is Daytime": "Yes" if is_daytime else "No"
    }

# -------- Streamlit UI --------
st.set_page_config(page_title="Wildfire Risk Predictor", layout="centered")
st.title("\U0001F525 Wildfire Risk Predictor")

st.subheader("📍 Select Location")
def_lat, def_lon = 30.2672, -97.7431
m = folium.Map(location=[def_lat, def_lon], zoom_start=6)
m.add_child(folium.LatLngPopup())
output = st_folium(m, height=400, width=700)
# Ensure map click fallback is safe
clicked = output["last_clicked"] if isinstance(output, dict) and output.get("last_clicked") else {}

selected_lat = clicked.get("lat", def_lat)
selected_lon = clicked.get("lng", def_lon)


st.write(f"**Latitude:** {round(selected_lat, 4)}  **Longitude:** {round(selected_lon, 4)}")

input_mode = st.radio("Select Brightness/FRP Input Mode:", ["Manual", "Default Estimate", "From FIRMS File"])

if input_mode == "Manual":
    brightness = st.slider("Brightness (Kelvin)", 300, 400, 320)
    frp = st.slider("Fire Radiative Power (FRP)", 0, 500, 220)
elif input_mode == "Default Estimate":
    brightness = 330.0
    frp = 200.0
else:
    fire_data = get_nearest_fire_data(selected_lat, selected_lon)
    if fire_data:
        brightness = fire_data["brightness"]
        frp = fire_data["frp"]
        st.success(f"🔥 FIRMS fire detected nearby! Brightness={brightness}, FRP={frp}")
    else:
        brightness = 305.0
        frp = 10
        st.warning("No FIRMS fire nearby — using default values")

if st.button("Predict Fire Risk"):
    result = predict_fire_risk_verbose(selected_lat, selected_lon, brightness, frp)
    if result:
        st.success(f"\U0001F525 Fire Risk: {result['Fire Risk']}")
        st.metric("Confidence", result["Confidence"])
        st.metric("Temperature", result["Temperature"])
        st.metric("Humidity", result["Humidity"])
        st.metric("Wind Speed", result["Wind Speed"])
        st.metric("Weather", result["Weather"])
        st.metric("Is Daytime", result["Is Daytime"])
    else:
        st.error("❌ Failed to retrieve weather data.")
