import requests
import sqlite3


API_URL = "https://api.open-meteo.com/v1/forecast"
DATABASE = "data/weather.db"

PARAMS = {
    "latitude": 47.8095,
    "longitude": 13.0550,
    "hourly": "temperature_2m,wind_speed_10m",
    "past_days": 2,
    "forecast_days": 1,
    "timezone": "Europe/Vienna"
}


def fetch_hourly_weather():
    response = requests.get(
        API_URL,
        params=PARAMS,
        timeout=10
    )

    response.raise_for_status()

    data = response.json()

    times = data["hourly"]["time"]
    temperatures = data["hourly"]["temperature_2m"]
    wind_speeds = data["hourly"]["wind_speed_10m"]

    observations = []

    for time, temperature, wind_speed in zip(
        times,
        temperatures,
        wind_speeds
    ):
        observations.append(
            (time, temperature, wind_speed)
        )

    return observations


def save_observations(observations):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    inserted_count = 0

    for observation in observations:
        cursor.execute("""
            INSERT OR IGNORE INTO weather_observations (
                time,
                temperature,
                wind_speed
            )
            VALUES (?, ?, ?)
        """, observation)

        if cursor.rowcount == 1:
            inserted_count += 1

    connection.commit()
    connection.close()

    return inserted_count


def main():
    observations = fetch_hourly_weather()

    inserted_count = save_observations(observations)

    print(
        f"{inserted_count} hourly observations saved."
    )


if __name__ == "__main__":
    main()