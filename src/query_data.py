import sqlite3

DATABASE = "data/weather.db"

connection = sqlite3.connect(DATABASE)
cursor = connection.cursor()

# Alle Einträge anzeigen
cursor.execute("""
    SELECT id, time, temperature, wind_speed
    FROM weather_observations
    ORDER BY id DESC
""")

rows = cursor.fetchall()

print("--- All observations ---")

for row in rows:
    print(row)


# Durchschnittswerte berechnen
cursor.execute("""
    SELECT
        AVG(temperature),
        MIN(temperature),
        MAX(temperature),
        AVG(wind_speed)
    FROM weather_observations
""")

stats = cursor.fetchone()

print("\n--- Weather statistics ---")
print(f"Average temperature: {stats[0]:.1f} °C")
print(f"Minimum temperature: {stats[1]:.1f} °C")
print(f"Maximum temperature: {stats[2]:.1f} °C")
print(f"Average wind speed: {stats[3]:.1f} km/h")

connection.close()