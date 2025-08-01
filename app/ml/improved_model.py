import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.utils import resample
from sklearn.metrics import precision_score, recall_score, f1_score, confusion_matrix
import matplotlib.pyplot as plt

# 📦 Load Data
df = pd.read_csv("tamil_nadu_weather_synthetic.csv")

# 🧹 Preprocessing
df['date'] = pd.to_datetime(df['date'])
df['time'] = pd.to_datetime(df['time'], format='%H:%M').dt.hour  # Use hour as feature

# 📊 Feature and Label
X = df[['temperature', 'humidity', 'time']]  # Add more if needed
y = df['did_rain']

# ⚖️ Balance Dataset (Upsample)
df_combined = pd.concat([X, y], axis=1)
majority = df_combined[df_combined.did_rain == 0]
minority = df_combined[df_combined.did_rain == 1]
minority_upsampled = resample(minority, replace=True, n_samples=len(majority), random_state=42)
df_balanced = pd.concat([majority, minority_upsampled])

X = df_balanced[['temperature', 'humidity', 'time']]
y = df_balanced['did_rain']

# 🔀 Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 🤖 Train RandomForest Model
model = RandomForestClassifier(n_estimators=100, class_weight='balanced', random_state=42)
model.fit(X_train, y_train)

# 🔍 Predict with lower threshold to improve recall
y_probs = model.predict_proba(X_test)[:, 1]
threshold = 0.3  # You can adjust this
y_pred = (y_probs >= threshold).astype(int)

# 📈 Evaluate
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)

print("Precision:", precision)
print("Recall:", recall)
print("F1 Score:", f1)
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))

# 📊 Plotting
metrics = ['Precision', 'Recall', 'F1 Score']
scores = [precision, recall, f1]
colors = ['orange', 'green', 'blue']

plt.bar(metrics, scores, color=colors)
plt.ylim(0, 1)
plt.ylabel("Score")
plt.title("Improved Model Performance Metrics")
plt.savefig("model_performance_improved.png")
plt.show()
