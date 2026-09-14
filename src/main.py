import requests
import sqlite3


API_URL = "https://api.open-meteo.com/v1/forecast"

PARAMS = {
    "latitude": 47.8095,
    "longitude": 13.0550,
    "current": "temperature_2m,wind_speed_10m",
    "timezone": "Europe/Vienna"
}

DATABASE = "data/weather.db"


def fetch_weather():
    response = requests.get(
        API_URL,
        params=PARAMS,
        timeout=10
    )

    response.raise_for_status()

    data = response.json()

    current = data["current"]

    weather = {
        "time": current["time"],
        "temperature": current["temperature_2m"],
        "wind_speed": current["wind_speed_10m"]
    }

    return weather


def create_database():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS weather_observations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            time TEXT NOT NULL UNIQUE,
            temperature REAL NOT NULL,
            wind_speed REAL NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def save_weather(weather):
    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    cursor.execute("""
    INSERT OR IGNORE INTO weather_observations (
        time,
        temperature,
        wind_speed
    )
    VALUES (?, ?, ?)
""", (
    weather["time"],
    weather["temperature"],
    weather["wind_speed"]
))

    connection.commit()
    connection.close()


def main():
    create_database()

    weather = fetch_weather()

    save_weather(weather)

    print("Weather data saved successfully.")
    print(f"Time: {weather['time']}")
    print(f"Temperature: {weather['temperature']} °C")
    print(f"Wind speed: {weather['wind_speed']} km/h")


if __name__ == "__main__":
    main()