import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib
from datetime import datetime

# Load dataset
df = pd.read_csv("tamil_nadu_weather_synthetic.csv")

# Preprocess
df['date'] = pd.to_datetime(df['date'])
df['time'] = pd.to_datetime(df['time'], format='%H:%M').dt.strftime('%H:%M')
df['day'] = df['date'].dt.day
df['month'] = df['date'].dt.month
df['year'] = df['date'].dt.year
df['hour'] = pd.to_datetime(df['time'], format='%H:%M').dt.hour

# Encode districts
le = LabelEncoder()
df['district_encoded'] = le.fit_transform(df['district_name'])

# Training
features = ['district_encoded', 'day', 'month', 'year', 'hour', 'temperature', 'humidity']
X = df[features]
y = df['did_rain']

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# Save model & encoder
joblib.dump(model, "rain_model.pkl")
joblib.dump(le, "district_encoder.pkl")

# Prediction function
def     isRain(date: str, district: str, time: str) -> str:
    try:
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        time_obj = datetime.strptime(time, "%H:%M")
    except ValueError:
        return "❌ Invalid format. Use YYYY-MM-DD and HH:MM"

    if district not in le.classes_:
        return f"❌ Unknown district: {district}"

    # Extract features
    day = date_obj.day
    month = date_obj.month
    year = date_obj.year
    hour = time_obj.hour
    time_str = time_obj.strftime('%H:%M')
    district_encoded = le.transform([district])[0]

    # Check for exact match in training data
    match = df[
        (df['district_name'] == district) &
        (df['date'] == date_obj) &
        (df['time'] == time_str)
    ]

    if not match.empty:
        temperature = match.iloc[0]['temperature']
        humidity = match.iloc[0]['humidity']
    else:
        # Estimate temp/humidity based on month (simple monsoon logic)
        if month in [6, 7, 8, 9, 10]:  # Monsoon
            temperature = 26.0
            humidity = 90.0
        elif month in [11, 12, 1]:  # Post-monsoon / winter
            temperature = 23.0
            humidity = 80.0
        else:  # Summer / dry season
            temperature = 35.0
            humidity = 55.0

    # Create input row
    row = pd.DataFrame([{
        'district_encoded': district_encoded,
        'day': day,
        'month': month,
        'year': year,
        'hour': hour,
        'temperature': temperature,
        'humidity': humidity
    }])

    prediction = model.predict(row)[0]
    return "🌧️ Rain Expected" if prediction == 1 else "☀️ No Rain"