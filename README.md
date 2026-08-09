# 🌤️ Weather Prediction & Analytics Platform

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://streamlit.io/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![Scikit-Learn](https://img.shields.io/badge/scikit--learn-%23F7931E.svg?style=flat&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An end-to-end Machine Learning web application designed to predict temperatures, analyze meteorological features, and visualize spatial-temporal weather patterns interactively.

---

## 🚀 Live Demo & Deployment

- **Live Web App**: *Deploying on Streamlit Community Cloud (Follow instructions below)*
- **GitHub Repository**: [Dhanush-734/WeatherPredictionProject](https://github.com/Dhanush-734/WeatherPredictionProject)

---

## 🔥 Key Features

- **📊 Exploratory Data Analysis (EDA)**: Interactive data visualizations powered by Plotly and Matplotlib for feature distributions and correlations.
- **🤖 Machine Learning Model**: Trained regression pipelines to accurately forecast temperature based on humidity, atmospheric pressure, wind speed, and seasonal metrics.
- **🗺️ Geo-Spatial Visualizations**: Interactive map interfaces built with Folium & Geopandas for real-time region-based weather trends.
- **🔮 Real-Time Predictions**: User-friendly Streamlit dashboard allowing real-time input parameter adjustments and instant ML model inferences.

---

## 🛠️ Tech Stack & Libraries

- **Language**: Python 3.10+
- **Machine Learning**: `scikit-learn`, `joblib`, `numpy`, `pandas`
- **Web Interface**: `streamlit`, `streamlit-folium`, `streamlit-plotly-events`
- **Visualization**: `plotly`, `matplotlib`, `folium`, `geopandas`

---

## 📁 Repository Structure

```
WeatherPredictionProject/
├── dataset/            # Raw and preprocessed weather data
├── models/             # Trained ML models and scalar artifacts (.pkl / .joblib)
├── notebooks/          # Step-by-step EDA, model evaluation, and inference notebooks
├── output/             # Generated charts, prediction outputs, and reports
├── streamlit/          # Streamlit web application source code
│   ├── app.py          # Main entry point for Streamlit Community Cloud
│   ├── style.css       # Custom UI CSS styling
│   └── pages/          # Multi-page dashboard components
├── train_model.py      # Standalone model training script
├── requirements.txt    # Production dependencies
└── Dockerfile          # Container configuration
```

---

## ⚡ Quick Start (Local Setup)

### 1. Clone the repository
```bash
git clone https://github.com/Dhanush-734/WeatherPredictionProject.git
cd WeatherPredictionProject
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. (Optional) Train the model
```bash
python train_model.py
```

### 4. Run the Streamlit Web Application
```bash
streamlit run streamlit/app.py
```

---

## 🌐 Deployment Instructions (Streamlit Community Cloud)

1. Log in to [Streamlit Community Cloud](https://share.streamlit.io/) with your GitHub account.
2. Click **New App** -> Select Repository: `Dhanush-734/WeatherPredictionProject`.
3. Set **Branch**: `main`.
4. Set **Main file path**: `streamlit/app.py`.
5. Click **Deploy!**

---

## 📄 License

Distributed under the MIT License. Feel free to star ⭐️ the repository and use it for learning!
