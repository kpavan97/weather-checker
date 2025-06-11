import streamlit as st
import requests
from datetime import datetime
from streamlit_lottie import st_lottie
import json
import os
import time

# Load Lottie animations
def load_lottie_file(filepath: str):
    if not os.path.exists(filepath):
        st.error(f"Animation file not found: {filepath}")
        return None
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

sunny_anim = load_lottie_file("sunny.json")
rainy_anim = load_lottie_file("rainy.json")
cloudy_anim = load_lottie_file("cloudy.json")

# Streamlit page config
st.set_page_config(page_title="Weather Checker", page_icon="🌤️", layout="centered")

# Custom CSS styling
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    .stButton>button {
        border-radius: 20px;
        padding: 10px 24px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: bold;
        border: none;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    .weather-card {
        border-radius: 15px;
        padding: 25px;
        background: white;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        margin-top: 20px;
    }
    .temperature {
        font-size: 3rem;
        font-weight: bold;
        color: #333;
    }
    .weather-desc {
        font-size: 1.2rem;
        color: #666;
    }
    .city-name {
        font-size: 2rem;
        font-weight: bold;
        color: #444;
        margin-bottom: 5px;
    }
    .details {
        display: flex;
        justify-content: space-between;
        margin-top: 20px;
    }
    .detail-item {
        text-align: center;
        padding: 10px;
        border-radius: 10px;
        background: rgba(255, 255, 255, 0.7);
        flex: 1;
        margin: 0 5px;
    }
    .detail-value {
        font-weight: bold;
        font-size: 1.1rem;
    }
    .detail-label {
        font-size: 0.8rem;
        color: #666;
    }
</style>
""", unsafe_allow_html=True)

# UI
st.title("🌤️ Weather Checker")
st.markdown("Check current weather conditions for any city, town or village in India")

indian_places = sorted([
    "Hyderabad", "Visakhapatnam", "Warangal", "Sattenapalle",
    "Bhimavaram", "Tirupati", "Amalapuram", "Eluru", "Nellore",
    "Tadepalligudem", "Ongole", "Gudur", "Kodad", "Palamaner",
    "Kakinada", "Karimnagar", "Mancherial", "Yellandu", "Rajahmundry",
    "Anantapur", "Kadapa", "Tenali", "Machilipatnam"
])

city = st.selectbox("Select a place in India", indian_places)

# Get API key from Streamlit secrets
API_KEY = st.secrets["API_KEY"]
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

# Function to get weather
def get_weather(city):
    params = {
        'q': f"{city},IN",
        'appid': API_KEY,
        'units': 'metric'
    }
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Search
if st.button("Get Weather"):
    if city:
        with st.spinner("Fetching weather data..."):
            weather_data = get_weather(city)
            time.sleep(1)

            if weather_data:
                temp = weather_data['main']['temp']
                feels_like = weather_data['main']['feels_like']
                humidity = weather_data['main']['humidity']
                wind_speed = weather_data['wind']['speed']
                weather_desc = weather_data['weather'][0]['description'].title()
                weather_main = weather_data['weather'][0]['main']
                city_name = weather_data['name']
                country = weather_data['sys']['country']
                sunrise = datetime.fromtimestamp(weather_data['sys']['sunrise']).strftime('%H:%M')
                sunset = datetime.fromtimestamp(weather_data['sys']['sunset']).strftime('%H:%M')

                with st.container():
                    st.markdown(f'<div class="weather-card">', unsafe_allow_html=True)
                    col1, col2 = st.columns([1, 2])

                    with col1:
                        if "rain" in weather_desc.lower():
                            st_lottie(rainy_anim, height=150, key="rain")
                        elif "cloud" in weather_desc.lower():
                            st_lottie(cloudy_anim, height=150, key="cloud")
                        else:
                            st_lottie(sunny_anim, height=150, key="sun")

                    with col2:
                        st.markdown(f'<div class="city-name">{city_name}, {country}</div>', unsafe_allow_html=True)
                        st.markdown(f'<div class="temperature">{temp}°C</div>', unsafe_allow_html=True)
                        st.markdown(f'<div class="weather-desc">{weather_desc}</div>', unsafe_allow_html=True)
                        st.markdown(f'<div>Feels like: {feels_like}°C</div>', unsafe_allow_html=True)

                    st.markdown('<div class="details">', unsafe_allow_html=True)
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.markdown(f"""
                            <div class="detail-item">
                                <div class="detail-value">💧 {humidity}%</div>
                                <div class="detail-label">Humidity</div>
                            </div>
                        """, unsafe_allow_html=True)
                    with col2:
                        st.markdown(f"""
                            <div class="detail-item">
                                <div class="detail-value">🌬️ {wind_speed} m/s</div>
                                <div class="detail-label">Wind Speed</div>
                            </div>
                        """, unsafe_allow_html=True)
                    with col3:
                        st.markdown(f"""
                            <div class="detail-item">
                                <div class="detail-value">🌅 {sunrise}</div>
                                <div class="detail-label">Sunrise</div>
                            </div>
                        """, unsafe_allow_html=True)
                    with col4:
                        st.markdown(f"""
                            <div class="detail-item">
                                <div class="detail-value">🌇 {sunset}</div>
                                <div class="detail-label">Sunset</div>
                            </div>
                        """, unsafe_allow_html=True)

                    st.markdown('</div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.error("City not found. Please try another.")
