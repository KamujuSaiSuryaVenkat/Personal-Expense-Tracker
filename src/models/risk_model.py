import pandas as pd

from sklearn.model_selection import train_test_split

from sklearn.tree import DecisionTreeClassifier

from sklearn.metrics import (
    accuracy_score,
    classification_report
)


# ---------------------------------------------------
# CREATE RISK LABELS
# ---------------------------------------------------

def create_risk_labels(df):

    risk_levels = []

    for _, row in df.iterrows():

        if (
            row["Temperature"] >= 40
            or row["RainProbability"] >= 80
            or row["WindSpeed"] >= 20
        ):

            risk_levels.append("HIGH")

        elif (
            row["Temperature"] >= 34
            or row["Humidity"] >= 70
        ):

            risk_levels.append("MEDIUM")

        else:

            risk_levels.append("LOW")

    df["RiskLevel"] = risk_levels

    return df


# ---------------------------------------------------
# TRAIN MACHINE LEARNING MODEL
# ---------------------------------------------------

def train_model(df):

    features = df[
        [
            "Temperature",
            "Humidity",
            "WindSpeed",
            "RainProbability",
            "Pressure"
        ]
    ]

    target = df["RiskLevel"]

    X_train, X_test, y_train, y_test = train_test_split(
        features,
        target,
        test_size=0.2,
        random_state=42
    )

    model = DecisionTreeClassifier()

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    accuracy = accuracy_score(
        y_test,
        predictions
    )

    report = classification_report(
        y_test,
        predictions
    )

    return model, accuracy, report


# ---------------------------------------------------
# PREDICT WEATHER RISK
# ---------------------------------------------------

def predict_weather_risk(
    model,
    temperature,
    humidity,
    wind_speed,
    rain_probability,
    pressure
):

    input_data = [[
        temperature,
        humidity,
        wind_speed,
        rain_probability,
        pressure
    ]]

    prediction = model.predict(input_data)

    return prediction[0]