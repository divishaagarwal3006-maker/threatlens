from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
import joblib
import pandas as pd

# Dataset: emails.csv with columns: text, label (phishing/safe)
data = pd.read_csv("emails.csv")
model = make_pipeline(TfidfVectorizer(), MultinomialNB())
model.fit(data["text"], data["label"])
joblib.dump(model, "email_model.pkl")
