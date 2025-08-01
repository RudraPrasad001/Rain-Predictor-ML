from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, precision_score, recall_score, f1_score
from sklearn.model_selection import train_test_split
from sklearn.utils import resample
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Assume you have preprocessed X_train, y_train, X_test, y_test


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
# 🔁 Upsample rain class
train_data = pd.concat([X_train, y_train], axis=1)
rain = train_data[train_data['did_rain'] == 1]
no_rain = train_data[train_data['did_rain'] == 0]
rain_upsampled = resample(rain, replace=True, n_samples=len(no_rain), random_state=42)
upsampled_data = pd.concat([no_rain, rain_upsampled])
X_train = upsampled_data.drop('did_rain', axis=1)
y_train = upsampled_data['did_rain']

# 🔍 Train model
clf = RandomForestClassifier(class_weight="balanced", random_state=42)
clf.fit(X_train, y_train)

# 🎯 Predict and evaluate
y_pred_proba = clf.predict_proba(X_test)[:, 1]
y_pred = (y_pred_proba > 0.3).astype(int)

precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
cm = confusion_matrix(y_test, y_pred)

# 📊 Bar chart
plt.figure(figsize=(6, 4))
plt.bar(['Precision', 'Recall', 'F1 Score'], [precision, recall, f1], color=['orange', 'green', 'blue'])
plt.title('Model Performance Metrics')
plt.ylabel('Score')
plt.ylim(0, 1)
plt.tight_layout()
plt.savefig("performance_metrics.png")
plt.close()

# 📊 Confusion matrix
plt.figure(figsize=(5, 4))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=["No Rain", "Rain"], yticklabels=["No Rain", "Rain"])
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Confusion Matrix')
plt.tight_layout()
plt.savefig("confusion_matrix.png")
plt.close()

print("Precision:", precision)
print("Recall:", recall)
print("F1 Score:", f1)
