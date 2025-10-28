import streamlit as st
import requests

# ---------------- Page config ----------------
st.set_page_config(page_title="Smart Weather Prediction App", page_icon="☁️", layout="centered")

# ---------------- API key (WeatherAPI) ----------------
API_KEY = "268c814b5a844219a10161018252810"  # using the key you provided

# ---------------- Title + short theory (visible immediately) ----------------
st.title("🌥️  Smart Weather Prediction App")


st.write(
    "Welcome to the Smart Weather Prediction App.\n\n"
    "Just type the name of any city and get the current weather conditions instantly.\n"
    "You will also receive a clear, human-friendly suggestion based on the live weather —"
    "so you know how to plan your day."
)



st.write("---")

# ---------------- Suggestion logic (neutral tone + precaution) ----------------
def smart_suggestion(temp_c: float, condition: str, humidity: int) -> str:
    c = (condition or "").lower()

    if "rain" in c or "drizzle" in c or "shower" in c:
        return "Light rain or showers are expected — it is advisable to carry an umbrella or a light raincoat."
    if "snow" in c or "sleet" in c:
        return "Snow or sleet conditions — wearing warm clothing and taking care on slippery surfaces is recommended."
    if "clear" in c or "sun" in c:
        if temp_c >= 35:
            return "Clear and hot — it is recommended to stay hydrated and limit prolonged sun exposure."
        if temp_c <= 5:
            return "Clear but cold — wearing a warm layer is advisable."
        return "Clear skies — conditions are pleasant for outdoor activities."
    if "cloud" in c or "overcast" in c:
        return "Cloudy conditions — a light layer is advisable for comfort."
    if humidity is not None and humidity >= 80:
        if temp_c >= 30:
            return "High humidity and warm temperature — it may feel muggy; keeping hydrated is recommended."
        return "High humidity — the air may feel heavy; avoid strenuous exertion if you feel uncomfortable."
    return "Weather appears moderate — normal clothing and routine activities are appropriate."

# ---------------- Input & validation ----------------
city = st.text_input("🏙️ Enter city name (e.g. London, Delhi, New York)")

if not city.strip():
    st.info("Please enter a city name to get the current weather.")

get = st.button("Get Weather")

# ---------------- Fetch & display ----------------
if get:
    city_clean = city.strip()
    if not city_clean:
        st.warning("Please enter a city name.")
    else:
        url = f"https://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city_clean}"
        try:
            res = requests.get(url, timeout=8)
            data = res.json()
        except requests.exceptions.RequestException:
            st.error("Network error while contacting the weather service. Please try again.")
        else:
            # Friendly error when city not found or API returns an error
            if "error" in data:
                st.error("Oops! Couldn’t find that city — please check the spelling and try again 😊")
                # optional debug line (comment out if you don't want debug info)
                # st.write("DEBUG:", data.get("error", {}).get("message", data))
            else:
                # Extract required fields
                temp_c = data["current"].get("temp_c")
                condition = data["current"].get("condition", {}).get("text", "")
                humidity = data["current"].get("humidity")

                # Header
                st.subheader(f"📍 Weather in {city_clean.title()}")

                # Clean stacked result block
                st.write(f"**Temperature:** {temp_c} °C")
                st.write(f"**Condition:** {condition}")
                st.write(f"**Humidity:** {humidity}%")

                # Suggestion (merged with precaution)
                suggestion = smart_suggestion(temp_c, condition, humidity)
                st.success(suggestion)
