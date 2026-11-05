import streamlit as st
import pandas as pd

st.set_page_config(page_title="AtmoSync", layout="wide")

st.title("🌤️ AtmoSync")
st.subheader("Micro-Climate Analytics Dashboard")

st.write("Welcome to our Weather Analytics Project!")

df = pd.read_csv("Cleaned_Weather_Data.csv")

st.success("Weather data loaded successfully!")

st.dataframe(df)
import plotly.express as px

st.subheader("🌡️ Temperature Comparison")

fig = px.bar(
    df,
    x="location",
    y="temperature_c",
    color="temperature_c",
    title="Temperature by Location",
    labels={
        "location": "Location",
        "temperature_c": "Temperature (°C)"
    }
)

st.plotly_chart(fig, use_container_width=True)
st.subheader("💧 Humidity Comparison")

fig_humidity = px.bar(
    df,
    x="location",
    y="humidity_percent",
    color="humidity_percent",
    title="Humidity by Location",
    labels={
        "location": "Location",
        "humidity_percent": "Humidity (%)"
    },
    color_continuous_scale="Blues"
)

st.plotly_chart(fig_humidity, use_container_width=True)
st.subheader("📍 Location-wise Weather Comparison")

comparison = df[
    ["location", "temperature_c", "humidity_percent", "wind_speed_kmh"]
].copy()

comparison.columns = [
    "Location",
    "Temperature (°C)",
    "Humidity (%)",
    "Wind Speed (km/h)"
]

st.dataframe(comparison, use_container_width=True)
st.subheader("🌡️ Location-wise Temperature Heatmap")

heatmap_data = df.set_index("location")[["temperature_c"]]

fig_heatmap = px.imshow(
    heatmap_data,
    labels={
        "x": "Weather Parameter",
        "y": "Location",
        "color": "Temperature (°C)"
    },
    color_continuous_scale="RdYlBu_r",
    text_auto=True,
    aspect="auto",
    title="Temperature Heatmap"
)

st.plotly_chart(fig_heatmap, use_container_width=True)
st.subheader("📍 Select Location")

selected_location = st.selectbox(
    "Choose a location:",
    df["location"].unique()
)

location_data = df[df["location"] == selected_location]

st.write("Weather Details for:", selected_location)

st.dataframe(location_data, use_container_width=True)
st.subheader("📊 Weather Summary")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Average Temperature",
        f"{df['temperature_c'].mean():.1f} °C"
    )

with col2:
    st.metric(
        "Average Humidity",
        f"{df['humidity_percent'].mean():.1f}%"
    )

with col3:
    st.metric(
        "Total Locations",
        df["location"].nunique()
    )
st.subheader("📥 Download Weather Data")

csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Cleaned Weather Data",
    data=csv,
    file_name="AtmoSync_Weather_Data.csv",
    mime="text/csv"
)
import requests

st.subheader("🔎 Search Weather Anywhere in India")

city = st.text_input("Enter City or Location")

if st.button("Search Weather"):
    if city.strip():
        url = "https://geocoding-api.open-meteo.com/v1/search"

        params = {
            "name": city,
            "count": 10,
            "countryCode": "IN",
            "language": "en",
            "format": "json"
        }

        try:
            response = requests.get(
                url, params=params, timeout=15
            )
            response.raise_for_status()

            results = response.json().get("results", [])

            if results:
                place = results[0]

                st.success(
                    f"Location Found: {place['name']}"
                )

                weather_url = "https://api.open-meteo.com/v1/forecast"

                weather_params = {
                    "latitude": place["latitude"],
                    "longitude": place["longitude"],
                    "current": [
                        "temperature_2m",
                        "relative_humidity_2m",
                        "wind_speed_10m",
                        "precipitation"
                    ]
                }

                weather_response = requests.get(
                    weather_url,
                    params=weather_params,
                    timeout=15
                )
                weather_response.raise_for_status()

                weather = weather_response.json()["current"]

                col1, col2 = st.columns(2)

                with col1:
                    st.metric("🌡️ Temperature",
                              f"{weather['temperature_2m']} °C")
                    st.metric("💨 Wind Speed",
                              f"{weather['wind_speed_10m']} km/h")

                with col2:
                    st.metric("💧 Humidity",
                              f"{weather['relative_humidity_2m']}%")
                    st.metric("🌧️ Precipitation",
                              f"{weather['precipitation']} mm")

                st.caption(f"Weather time: {weather['time']}")
            else:
                st.warning("Location not found!")

        except requests.RequestException:
            st.error("Location search failed. Try again.")
    else:
        st.warning("Please enter a location.")

st.divider()

st.subheader("⚖️ Compare Two Locations")

city1 = st.text_input(
    "Enter First Location",
    value="Bareilly"
)

city2 = st.text_input(
    "Enter Second Location",
    value="Lucknow"
)

compare_button = st.button("Compare Weather")
if compare_button:

    def get_weather(city):
        geo_url = "https://geocoding-api.open-meteo.com/v1/search"

        geo_response = requests.get(
            geo_url,
            params={
                "name": city,
                "count": 1,
                "countryCode": "IN"
            },
            timeout=15
        )
        geo_response.raise_for_status()

        places = geo_response.json().get("results", [])

        if not places:
            return None

        place = places[0]

        weather_response = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": place["latitude"],
                "longitude": place["longitude"],
                "current": [
                    "temperature_2m",
                    "relative_humidity_2m",
                    "wind_speed_10m"
                ]
            },
            timeout=15
        )
        weather_response.raise_for_status()

        return weather_response.json()["current"]

    if not city1.strip() or not city2.strip():
        st.warning("Please enter both locations.")
    else:
        try:
            weather1 = get_weather(city1)
            weather2 = get_weather(city2)

            if weather1 and weather2:
                comparison_df = pd.DataFrame({
                    "Location": [city1, city2],
                    "Temperature (°C)": [
                        weather1["temperature_2m"],
                        weather2["temperature_2m"]
                    ],
                    "Humidity (%)": [
                        weather1["relative_humidity_2m"],
                        weather2["relative_humidity_2m"]
                    ],
                    "Wind Speed (km/h)": [
                        weather1["wind_speed_10m"],
                        weather2["wind_speed_10m"]
                    ]
                })

                st.success("Weather Comparison Ready!")
                st.dataframe(
                    comparison_df,
                    use_container_width=True
                )
                st.subheader("📊 Weather Comparison Graph")

                graph_data = comparison_df.melt(
                    id_vars="Location",
                    value_vars=[
                        "Temperature (°C)",
                        "Humidity (%)",
                        "Wind Speed (km/h)"
                    ],
                    var_name="Weather Parameter",
                    value_name="Value"
                )
                fig_compare = px.bar(
                    graph_data,
                    x="Location",
                    y="Value",
                    color="Location",
                    facet_col="Weather Parameter",
                    facet_col_wrap=3,
                    title="Location-wise Weather Comparison"
                )

                fig_compare.update_yaxes(matches=None)

                st.plotly_chart(
                    fig_compare,
                    use_container_width=True
                )
            else:
                st.warning("One or both locations not found.")

        except requests.RequestException:
            st.error("Unable to fetch weather data.")
