from fastapi import FastAPI
import joblib, pandas as pd

art = joblib.load("models/ids_rf.joblib")
app = FastAPI(title="IoT Intrusion Detection")

@app.post("/predict")
def predict(flow: dict):
    row = pd.DataFrame([flow]).reindex(columns=art["columns"])
    row[art["cats"]] = art["encoder"].transform(row[art["cats"]].astype(str))
    pred = art["model"].predict(row)[0]
    prob = art["model"].predict_proba(row).max()
    return {"prediction": pred, "confidence": round(float(prob), 4)}