import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import make_pipeline
from sklearn.metrics import classification_report

# Load dataset
data = pd.read_csv("emails.csv")
data.dropna(subset=["text_combined", "label"], inplace=True)

X = data["text_combined"]  # ← your column name
y = data["label"]

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Improved model
model = make_pipeline(
    TfidfVectorizer(
        ngram_range=(1, 2),
        max_features=10000,
        sublinear_tf=True,
        stop_words='english'
    ),
    RandomForestClassifier(n_estimators=100, random_state=42)
)

model.fit(X_train, y_train)

# Print accuracy
print(classification_report(y_test, model.predict(X_test)))

# Save model
joblib.dump(model, "email_model.pkl")
print("✅ Model saved!")