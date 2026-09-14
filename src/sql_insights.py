import sqlite3


DATABASE = "data/weather.db"

connection = sqlite3.connect(DATABASE)
cursor = connection.cursor()


# -----------------------------
# 1. Messungen über 20 °C
# -----------------------------

cursor.execute("""
    SELECT
        time,
        temperature,
        wind_speed
    FROM weather_observations
    WHERE temperature > 20
    ORDER BY temperature DESC
""")

warm_observations = cursor.fetchall()

print("--- Observations above 20 °C ---")

for row in warm_observations:
    print(row)


# -----------------------------
# 2. Die 5 windigsten Messungen
# -----------------------------

cursor.execute("""
    SELECT
        time,
        temperature,
        wind_speed
    FROM weather_observations
    ORDER BY wind_speed DESC
    LIMIT 5
""")

windiest_observations = cursor.fetchall()

print("\n--- Top 5 windiest observations ---")

for row in windiest_observations:
    print(row)


# -----------------------------
# 3. Anzahl heißerer Messungen
# -----------------------------

cursor.execute("""
    SELECT COUNT(*)
    FROM weather_observations
    WHERE temperature > 20
""")

warm_count = cursor.fetchone()[0]

print(
    f"\nNumber of observations above 20 °C: {warm_count}"
)


connection.close()