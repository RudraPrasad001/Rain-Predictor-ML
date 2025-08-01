import pandas as pd
import joblib
import matplotlib.pyplot as plt
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    precision_score,
    recall_score,
    f1_score,
    ConfusionMatrixDisplay
)
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

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

# Features & target
features = ['district_encoded', 'day', 'month', 'year', 'hour', 'temperature', 'humidity']
X = df[features]
y = df['did_rain']

# Split for evaluation
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Load model (or retrain if needed)
try:
    model = joblib.load("rain_model.pkl")
except FileNotFoundError:
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    joblib.dump(model, "rain_model.pkl")

# Predict
y_pred = model.predict(X_test)

# Accuracy
accuracy = accuracy_score(y_test, y_pred)
print(f"✅ Accuracy: {accuracy:.4f}")

# Confusion Matrix
cm = confusion_matrix(y_test, y_pred)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=["No Rain", "Rain"])
disp.plot(cmap="Blues")
plt.title("Confusion Matrix")
plt.savefig("matrix.png")


# Precision, Recall, F1
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)

# Bar Graph
plt.figure(figsize=(6, 4))
metrics = ['Precision', 'Recall', 'F1 Score']
scores = [precision, recall, f1]
plt.bar(metrics, scores, color=['orange', 'green', 'blue'])
plt.ylim(0, 1)
plt.title("Model Performance Metrics")
plt.ylabel("Score")
plt.savefig("performance_metrics.png")
plt.close()
