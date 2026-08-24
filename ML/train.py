import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

try:
    df = pd.read_parquet("clinical_notes.parquet")
    print(df.columns, sep="\n")
except Exception as e:
    print(e)
    print("File not loading. Check path")

if len(df) < 2:
    raise ValueError("At least two clinical notes are required for a split.")

X = df["clinical_note"]
y = df["icd_code"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
# train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)

vectorizer = TfidfVectorizer()

model = LogisticRegression(max_iter=1000)

X_train_vectorized = vectorizer.fit_transform(X_train)
X_test_vectorized = vectorizer.transform(X_test)

print("Training.. \n\n")
# train model

model.fit(X_train_vectorized, y_train)

print("Testing..")
# test model

accuracy = model.score(X_test_vectorized, y_test)

print(f"Accuracy: {accuracy}")
