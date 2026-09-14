import sqlite3

import pandas as pd
import matplotlib.pyplot as plt


DATABASE = "data/weather.db"


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


print("--- Weather data ---")
print(df.head())

print("\n--- Pandas statistics ---")
print(df.describe())


# Temperaturdiagramm
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


# Winddiagramm
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

plt.show()