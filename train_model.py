import os
import pickle
import joblib
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "dataset"
MODELS_DIR = ROOT / "models"
OUTPUT_DIR = ROOT / "output"
GRAPHS_DIR = OUTPUT_DIR / "graphs"
REPORTS_DIR = OUTPUT_DIR / "reports"

for path in [DATA_DIR, MODELS_DIR, OUTPUT_DIR, GRAPHS_DIR, REPORTS_DIR]:
    path.mkdir(parents=True, exist_ok=True)


def get_season(month):
    if month in [12, 1, 2]:
        return "Winter"
    elif month in [3, 4, 5]:
        return "Summer"
    elif month in [6, 7, 8]:
        return "Monsoon"
    else:
        return "Post-Monsoon"


def prepare_dataset(force_rebuild=False):
    featured_csv = DATA_DIR / "weather_featured.csv"
    clean_csv = DATA_DIR / "weather_clean.csv"
    raw_csv = DATA_DIR / "weather.csv"

    if not force_rebuild and featured_csv.exists():
        df = pd.read_csv(featured_csv)
        return df

    if raw_csv.exists():
        df = pd.read_csv(raw_csv)
        df.drop_duplicates(inplace=True)
        df.to_csv(clean_csv, index=False)
    elif clean_csv.exists():
        df = pd.read_csv(clean_csv)
        df.drop_duplicates(inplace=True)
    else:
        raise FileNotFoundError(f"Neither {raw_csv} nor {clean_csv} found.")

    df["Date"] = pd.to_datetime(df["Date"], format="mixed")
    df["Year"] = df["Date"].dt.year
    df["Month"] = df["Date"].dt.month
    df["Day"] = df["Date"].dt.day
    df["Hour"] = df["Date"].dt.hour
    df["DayOfWeek"] = df["Date"].dt.day_name()
    df["Season"] = df["Month"].apply(get_season)

    le_city = LabelEncoder()
    le_weather = LabelEncoder()
    le_day = LabelEncoder()
    le_season = LabelEncoder()

    le_city.fit(df["City"])
    le_weather.fit(df["Weather"])
    le_day.fit(df["DayOfWeek"])
    le_season.fit(df["Season"])

    joblib.dump(le_city, MODELS_DIR / "le_city.pkl")
    joblib.dump(le_weather, MODELS_DIR / "le_weather.pkl")
    joblib.dump(le_day, MODELS_DIR / "le_day.pkl")
    joblib.dump(le_season, MODELS_DIR / "le_season.pkl")

    df["City"] = le_city.transform(df["City"])
    df["Weather"] = le_weather.transform(df["Weather"])
    df["DayOfWeek"] = le_day.transform(df["DayOfWeek"])
    df["Season"] = le_season.transform(df["Season"])

    if "Date" in df.columns:
        df.drop("Date", axis=1, inplace=True)

    df.to_csv(featured_csv, index=False)
    return df


def train_model(df: pd.DataFrame):
    X = df.drop("Temperature", axis=1)
    y = df["Temperature"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    mae = mean_absolute_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)

    joblib.dump(model, MODELS_DIR / "weather_model.pkl")

    predictions_df = pd.DataFrame({"actual": y_test.values, "predicted": predictions})
    predictions_df.to_csv(OUTPUT_DIR / "predictions.csv", index=False)

    plt.figure(figsize=(6, 4))
    plt.scatter(y_test, predictions, alpha=0.5, color="skyblue")
    plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], color="red", linestyle="--")
    plt.xlabel("Actual Temperature")
    plt.ylabel("Predicted Temperature")
    plt.title("Actual vs Predicted Temperature")
    plt.tight_layout()
    plt.savefig(GRAPHS_DIR / "predictions_scatter.png", dpi=300)
    plt.close()

    with (REPORTS_DIR / "model_metrics.txt").open("w", encoding="utf-8") as fh:
        fh.write(f"MAE: {mae:.2f}\n")
        fh.write(f"R2: {r2:.3f}\n")

    print(f"Metrics - MAE: {mae:.2f}, R2: {r2:.3f}")


if __name__ == "__main__":
    df = prepare_dataset(force_rebuild=True)
    train_model(df)
    print("Training complete. Model saved to models/weather_model.pkl")
