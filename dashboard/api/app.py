from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd

app = FastAPI(title="GetAround Pricing API")

# Chargement du modèle
model = joblib.load("model.joblib")

# Définition du format de données attendu
class CarFeatures(BaseModel):
    model_key: str
    mileage: int
    engine_power: int
    fuel: str
    paint_color: str
    car_type: str
    private_parking_available: bool
    has_gps: bool
    has_air_conditioning: bool
    automatic_car: bool
    has_getaround_connect: bool
    has_speed_regulator: bool
    winter_tires: bool

@app.get("/")
def index():
    return {"message": "API opérationnelle. Allez sur /docs pour tester."}

@app.post("/predict")
def predict(features: CarFeatures):
    # Transformation en DataFrame pour le modèle
    data = pd.DataFrame([features.dict()])
    prediction = model.predict(data)
    return {"prediction": float(prediction[0])}