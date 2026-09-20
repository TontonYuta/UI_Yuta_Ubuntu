#!/usr/bin/env python3
"""
weather.py - Ultra-fast Open-Meteo Weather Fetcher for Conky Desktop Widgets
Clean typography & universal symbol support (no broken emoji glyphs)
"""

import sys
import os
import time
import json
import urllib.request

CACHE_FILE = os.path.expanduser("~/.cache/conky_weather.json")
CACHE_EXPIRY = 900  # 15 minutes

WMO_MAP = {
    0: ("Trời quang", "Clear Sky"),
    1: ("Ít mây", "Mainly Clear"),
    2: ("Có mây", "Partly Cloudy"),
    3: ("Nhiều mây", "Overcast"),
    45: ("Sương mù", "Fog"),
    48: ("Sương đọng", "Depositing Fog"),
    51: ("Mưa phùn nhẹ", "Light Drizzle"),
    53: ("Mưa phùn", "Moderate Drizzle"),
    55: ("Mưa phùn dày", "Dense Drizzle"),
    56: ("Mưa lạnh nhẹ", "Light Freezing Drizzle"),
    57: ("Mưa lạnh đặc", "Dense Freezing Drizzle"),
    61: ("Mưa rào nhẹ", "Slight Rain"),
    63: ("Mưa rào vừa", "Moderate Rain"),
    65: ("Mưa rào to", "Heavy Rain"),
    66: ("Mưa buốt nhẹ", "Light Freezing Rain"),
    67: ("Mưa buốt to", "Heavy Freezing Rain"),
    71: ("Tuyết rơi nhẹ", "Slight Snow"),
    73: ("Tuyết vừa", "Moderate Snow"),
    75: ("Tuyết dày", "Heavy Snow"),
    77: ("Mưa tuyết hạt", "Snow Grains"),
    80: ("Mưa rào rải rác", "Slight Showers"),
    81: ("Mưa rào vừa", "Moderate Showers"),
    82: ("Mưa rào xối xả", "Violent Showers"),
    85: ("Tuyết rào nhẹ", "Slight Snow Showers"),
    86: ("Tuyết rào dày", "Heavy Snow Showers"),
    95: ("Có sấm giông", "Thunderstorm"),
    96: ("Giông mưa đá nhẹ", "Thunderstorm w/ Hail"),
    99: ("Giông mưa đá mạnh", "Heavy Thunderstorm w/ Hail")
}

def get_location():
    try:
        req = urllib.request.Request("http://ip-api.com/json", headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=3) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            city = data.get("city", "Hà Nội")
            lat = data.get("lat", 21.0285)
            lon = data.get("lon", 105.8542)
            country = data.get("country", "Vietnam")
            return city, lat, lon, country
    except Exception:
        return "Hà Nội", 21.0285, 105.8542, "Vietnam"

def fetch_weather():
    city, lat, lon, country = get_location()
    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}&"
        f"current=temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,wind_speed_10m&"
        f"daily=temperature_2m_max,temperature_2m_min,precipitation_probability_max&"
        f"timezone=auto"
    )
    req = urllib.request.Request(url, headers={'User-Agent': 'ConkyWeatherWidget/1.0'})
    with urllib.request.urlopen(req, timeout=5) as resp:
        api_data = json.loads(resp.read().decode('utf-8'))
    
    current = api_data.get("current", {})
    daily = api_data.get("daily", {})
    
    w_code = current.get("weather_code", 0)
    vi_desc, en_desc = WMO_MAP.get(w_code, ("Có mây", "Partly Cloudy"))
    
    high = daily.get("temperature_2m_max", [0])[0] if daily.get("temperature_2m_max") else 0
    low = daily.get("temperature_2m_min", [0])[0] if daily.get("temperature_2m_min") else 0
    rain_prob = daily.get("precipitation_probability_max", [0])[0] if daily.get("precipitation_probability_max") else 0
    
    weather_dict = {
        "city": city,
        "country": country,
        "temp": round(current.get("temperature_2m", 0)),
        "feels_like": round(current.get("apparent_temperature", 0)),
        "humidity": current.get("relative_humidity_2m", 0),
        "wind": round(current.get("wind_speed_10m", 0)),
        "weather_code": w_code,
        "condition_vi": vi_desc,
        "condition_en": en_desc,
        "high": round(high),
        "low": round(low),
        "rain_prob": rain_prob,
        "updated_at": time.time()
    }
    
    os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(weather_dict, f, ensure_ascii=False, indent=2)
    
    return weather_dict

def load_data():
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            if time.time() - data.get("updated_at", 0) < CACHE_EXPIRY:
                return data
        except Exception:
            pass
    try:
        return fetch_weather()
    except Exception:
        if os.path.exists(CACHE_FILE):
            try:
                with open(CACHE_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {
            "city": "Hà Nội",
            "country": "Vietnam",
            "temp": 28,
            "feels_like": 30,
            "humidity": 80,
            "wind": 10,
            "condition_vi": "Thời tiết đẹp",
            "condition_en": "Partly Cloudy",
            "high": 32,
            "low": 25,
            "rain_prob": 20
        }

def main():
    arg = sys.argv[1] if len(sys.argv) > 1 else "--temp"
    data = load_data()
    
    if arg == "--temp":
        print(f"{data['temp']}°C")
    elif arg == "--temp-val":
        print(f"{data['temp']}°")
    elif arg == "--feels-like":
        print(f"{data['feels_like']}°C")
    elif arg == "--condition":
        print(data['condition_vi'])
    elif arg == "--condition-en":
        print(data['condition_en'])
    elif arg == "--city":
        print(data['city'])
    elif arg == "--high-low":
        print(f"H: {data['high']}°  L: {data['low']}°")
    elif arg == "--humidity":
        print(f"{data['humidity']}%")
    elif arg == "--wind":
        print(f"{data['wind']} km/h")
    elif arg == "--rain":
        print(f"{data['rain_prob']}%")
    elif arg == "--summary":
        print(f"{data['temp']}°C • {data['condition_vi']}")
    else:
        print(f"{data['temp']}°C")

if __name__ == "__main__":
    main()
