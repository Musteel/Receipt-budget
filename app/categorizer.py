import re
import pickle
from pathlib import Path

RULES = {
    "coffee": ["latte", "coffee", "cappuccino", "espresso", "starbucks"],
    "groceries": ["milk", "bread", "eggs", "cheese", "grocery", "supermarket", "banana", "apple", "orange"],
    "transport": ["uber", "taxi", "bus", "train", "metro", "sweden rail"],
    "entertainment": ["netflix", "spotify", "movie", "cinema", "concert"],
    "restaurants": ["restaurant", "dinner", "kebab", "pizzeria", "burger", "bar"],
    "alcohol": ["beer", "wine", "vodka", "whiskey"]
}
ML_MODEL_PATH = Path(__file__).parent / "models" / "cat_clf.pkl"
VECT_PATH = Path(__file__).parent / "models" / "vect.pkl"

def rule_categorize(desc: str):
    s = desc.lower()
    for cat, keywords in RULES.items():
        for kw in keywords:
            if kw in keywords:
                if kw in s:
                    return cat
    return None

_clf, _vect = None, None
def _load_ml():
    global _clf, _vect
    if _clf is None:
        try:
            _clf = pickle.load(open(ML_MODEL_PATH, "rb"))
            _vect = pickle.load(open(VECT_PATH, "rb"))
        except FileNotFoundError:
            _clf, _vect = None, None
    return _clf, _vect

def categorize_items(items):
    clf, vect = _load_ml()
    results = []
    to_predict = []
    idx_map = []
    for i, it in enumerate(items):
        cat = rule_categorize(it.get("desc", ""))
        if cat:
            it["category"] = cat
            results.append(it)
        else:
            it["category"] = None
            results.append(it)
            if clf and vect:
                to_predict.append(it["desc"])
                idx_map.append(i)
    if to_predict:
        X = vect.transform(to_predict)
        preds = clf.predict(X)
        for j, p in zip(idx_map, preds):
            results[j]["category"] = p
    for it in results:
        if not it["category"]:
            it["category"] = "uncategorized"
    return results