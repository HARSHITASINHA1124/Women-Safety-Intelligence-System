import joblib
from sklearn.linear_model import LogisticRegression

# ---------------- TRAINING DATA ----------------
# Features:
# [incident_count, avg_severity, night_flag, semantic_score]

X = [
    [1, 1.0, 0, 0.2],
    [2, 1.5, 0, 0.3],
    [3, 2.0, 1, 0.6],
    [4, 2.5, 1, 0.7],
    [6, 3.0, 1, 0.9],
]

# Labels:
# 0 = LOW, 1 = MODERATE, 2 = HIGH
y = [0, 0, 1, 2, 2]

# ---------------- MODEL ----------------
model = LogisticRegression(max_iter=1000)
model.fit(X, y)

# ---------------- SAVE ----------------
joblib.dump(model, "risk_model.pkl")

print("Risk model trained & saved")
