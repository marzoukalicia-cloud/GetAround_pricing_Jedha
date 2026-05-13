import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import Ridge
from sklearn.pipeline import Pipeline
import mlflow
import mlflow.sklearn

# 1. Chargement (on remonte d'un dossier pour aller dans api/)
df = pd.read_csv("../api/get_around_pricing_project.csv", index_col=0)

X = df.drop("rental_price_per_day", axis=1)
y = df["rental_price_per_day"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 2. Preprocessing (Numérique + Catégoriel)
numeric_features = ["mileage", "engine_power"]
categorical_features = ["model_key", "fuel", "paint_color", "car_type"]

preprocessor = ColumnTransformer(
    transformers=[
        ("num", StandardScaler(), numeric_features),
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features)
    ],
    remainder="passthrough"
)

# 3. Tracking MLflow
mlflow.set_experiment("GetAround_Pricing_Optimization")

with mlflow.start_run():
    # Pipeline
    model = Pipeline(steps=[
        ("preprocessor", preprocessor),
        ("regressor", Ridge(alpha=1.0))
    ])
    
    model.fit(X_train, y_train)
    r2_score = model.score(X_test, y_test)
    
    # Enregistrement dans MLflow
    mlflow.log_param("model_type", "Ridge")
    mlflow.log_metric("R2", r2_score)
    mlflow.sklearn.log_model(model, "pricing_model")
    
    print(f"✅ Entraînement réussi ! Score R2 : {r2_score:.4f}")