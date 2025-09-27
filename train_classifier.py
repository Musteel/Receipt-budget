import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import pickle
from pathlib import Path

df = pd.read_csv("train.csv")
vect = TfidfVectorizer(ngram_range=(1, 2))
X = vect.fit_transform(df['desc'])
y = df['category']
clf = LogisticRegression(max_iter=1000)
clf.fit(X, y)

out_dir = Path("app/models")
out_dir.mkdir(parents=True, exist_ok=True)
pickle.dump(clf, open(out_dir / "cat_clf.pkl", "wb"))
pickle.dump(vect, open(out_dir / "vect.pkl", "wb"))
print("Model and vectorizer saved.")