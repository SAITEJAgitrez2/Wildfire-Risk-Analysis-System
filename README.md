# 🔥 Wildfire Risk Predictor

This project is an AI-powered wildfire risk prediction system that uses real-time weather data and satellite fire detection (NASA FIRMS) to assess wildfire risk levels across regions. The system is accessible via an interactive Streamlit web interface.

## 🌐 Demo

![App UI](./demo_images/Screenshot%20\(188\).png)
![](./demo_images/Screenshot%20\(189\).png)
![](./demo_images/Screenshot%20\(190\).png)
![](./demo_images/Screenshot%20\(191\).png)

## 🚀 Features

- 🌍 **Interactive Map** to select location by clicking on any point
- ☁️ **Weather Integration** from OpenWeatherMap (temperature, humidity, wind speed, weather condition)
- 🔥 **NASA FIRMS** shapefile support for detecting real fires in the vicinity
- 🧠 **ML-Based Risk Prediction** (Random Forest, XGBoost, etc.)
- 🎯 Option to input **Brightness (K)** and **FRP** manually or automatically
- 📊 Confidence score and weather metadata displayed post-prediction

---

## 🛠 Tech Stack

- `Python`
- `Streamlit` for frontend
- `scikit-learn`, `xgboost` for model training
- `geopandas`, `shapely` for spatial data
- `OpenWeatherMap API` for live weather
- `NASA FIRMS` shapefile (MODIS 24h data)

---

This project is a practical application of core **Data Mining** principles, tailored for real-world environmental monitoring:

- 📊 **Data Collection & Integration**
  - Merged fire detection data (NASA FIRMS shapefiles) with real-time weather data (OpenWeatherMap API)
  - Geo-spatial and temporal merging ensures contextual richness in the data

- 🧹 **Preprocessing & Feature Engineering**
  - Cleaned and filtered fire records based on confidence levels
  - Engineered features such as:
    - Wind-Adjusted Brightness (`wind_factor`)
    - Day/Night Indicator (`is_daytime`)
    - One-hot encoded weather conditions
  - Binned `frp` values into categorical fire risk levels for classification

- 🔍 **Exploratory Data Analysis (EDA)**
  - Visualized variable distributions (e.g. temperature, humidity, wind)
  - Correlation heatmaps helped avoid multicollinearity and guided feature selection
  - Box plots revealed `frp` variance across weather types

- 📈 **Predictive Modeling**
  - Trained and compared classification models (Random Forest, XGBoost, Logistic Regression, SVM)
  - Used **Cross-Validation**, **Confusion Matrices**, and **Learning Curves** to ensure generalization and avoid overfitting
  - Encoded categorical outputs into numeric form (`LabelEncoder`) for ML compatibility

- ✅ **Model Evaluation**
  - Reported Accuracy, Precision, Recall, F1-score, and CV standard deviation
  - Final model deployed with ~99% test accuracy using XGBoost

- 🛰️ **Real-time Inference**
  - Integrated with live weather APIs for dynamic predictions
  - Optionally uses NASA FIRMS shapefile for nearby fire info (brightness & FRP) to boost accuracy

- 📌 **User Interaction Layer**
  - Built a fully interactive **Streamlit** dashboard with:
    - Map-based location picker
    - Manual/auto FRP/brightness selection
    - Real-time fire risk prediction and weather display

## 👥 Team Members

This project was developed as part of the Graduate Data Mining course at the University of North Texas.

| Name                     | Role                        | Contributions                                                                 |
|--------------------------|-----------------------------|-------------------------------------------------------------------------------|
| Sai Teja Narra Venkata   | ML Engineer / Streamlit Dev | Model training, API integration, Streamlit frontend, weather + FIRMS merging  |
| Hema Tummapala           | Data Scientist              | EDA, feature engineering, classification analysis, notebook organization      |
| Gudigopuram Varun Reddy              | Data Analyst                | EDA visualization, FRP-weather relation analysis, graphs and heatmaps         |
| Sai Karthik Yadav Dommala           | Data Engineer               | Raw data processing, confidence filtering, feature engineering pipelines      |
