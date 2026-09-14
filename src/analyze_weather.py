import sqlite3

import pandas as pd
import matplotlib.pyplot as plt


DATABASE = "data/weather.db"


# -----------------------------
# 1. Daten aus SQLite laden
# -----------------------------

connection = sqlite3.connect(DATABASE)

query = """
    SELECT
        time,
        temperature,
        wind_speed
    FROM weather_observations
    ORDER BY time
"""

df = pd.read_sql_query(
    query,
    connection,
    parse_dates=["time"]
)

connection.close()


# -----------------------------
# 2. Grundlegende Auswertung
# -----------------------------

print("--- Weather Analysis ---")
print(f"Number of observations: {len(df)}")

print(
    f"Average temperature: "
    f"{df['temperature'].mean():.1f} °C"
)

print(
    f"Minimum temperature: "
    f"{df['temperature'].min():.1f} °C"
)

print(
    f"Maximum temperature: "
    f"{df['temperature'].max():.1f} °C"
)

print(
    f"Average wind speed: "
    f"{df['wind_speed'].mean():.1f} km/h"
)

print(
    f"Maximum wind speed: "
    f"{df['wind_speed'].max():.1f} km/h"
)


# -----------------------------
# 3. Temperaturdiagramm
# -----------------------------

plt.figure(figsize=(10, 6))

plt.plot(
    df["time"],
    df["temperature"]
)

plt.title("Temperature in Salzburg")
plt.xlabel("Time")
plt.ylabel("Temperature (°C)")
plt.grid(True)

plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig(
    "output/temperature-history.png"
)

plt.close()


# -----------------------------
# 4. Winddiagramm
# -----------------------------

plt.figure(figsize=(10, 6))

plt.plot(
    df["time"],
    df["wind_speed"]
)

plt.title("Wind Speed in Salzburg")
plt.xlabel("Time")
plt.ylabel("Wind Speed (km/h)")
plt.grid(True)

plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig(
    "output/wind-speed-history.png"
)

plt.close()


# -----------------------------
# 5. Tägliche Zusammenfassung
# -----------------------------

df["date"] = df["time"].dt.date

daily_summary = df.groupby("date").agg(
    average_temperature=("temperature", "mean"),
    minimum_temperature=("temperature", "min"),
    maximum_temperature=("temperature", "max"),
    average_wind_speed=("wind_speed", "mean")
)

print("\n--- Daily Summary ---")
print(daily_summary.round(1))


# Als CSV speichern
daily_summary.to_csv(
    "output/daily-summary.csv"
)

print("\nAnalysis completed successfully.")