import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# ---------------------------------------------------
# CREATE OUTPUT FOLDER AUTOMATICALLY
# ---------------------------------------------------

os.makedirs("outputs/charts", exist_ok=True)

# Modern chart styling
sns.set_style("darkgrid")


# ---------------------------------------------------
# TEMPERATURE CHART
# ---------------------------------------------------

def temperature_chart(df):

    plt.figure(figsize=(10, 5))

    sns.barplot(
        x="City",
        y="Temperature",
        data=df
    )

    plt.title(
        "City vs Temperature",
        fontsize=16,
        fontweight="bold"
    )

    plt.xlabel("City", fontsize=12)

    plt.ylabel("Temperature (°C)", fontsize=12)

    plt.xticks(rotation=45)

    plt.tight_layout()

    plt.savefig(
        "outputs/charts/temperature_chart.png",
        dpi=300
    )

    plt.close()


# ---------------------------------------------------
# HUMIDITY CHART
# ---------------------------------------------------

def humidity_chart(df):

    plt.figure(figsize=(10, 5))

    sns.lineplot(
        x="City",
        y="Humidity",
        data=df,
        marker="o",
        linewidth=3
    )

    plt.title(
        "City vs Humidity",
        fontsize=16,
        fontweight="bold"
    )

    plt.xlabel("City", fontsize=12)

    plt.ylabel("Humidity (%)", fontsize=12)

    plt.xticks(rotation=45)

    plt.tight_layout()

    plt.savefig(
        "outputs/charts/humidity_chart.png",
        dpi=300
    )

    plt.close()


# ---------------------------------------------------
# RISK DISTRIBUTION CHART
# ---------------------------------------------------

def risk_distribution(df):

    plt.figure(figsize=(8, 5))

    sns.countplot(
        x="RiskLevel",
        data=df,
        order=["LOW", "MEDIUM", "HIGH"]
    )

    plt.title(
        "Weather Risk Distribution",
        fontsize=16,
        fontweight="bold"
    )

    plt.xlabel("Risk Level", fontsize=12)

    plt.ylabel("Count", fontsize=12)

    plt.tight_layout()

    plt.savefig(
        "outputs/charts/risk_distribution.png",
        dpi=300
    )

    plt.close()


# ---------------------------------------------------
# CORRELATION HEATMAP
# ---------------------------------------------------

def correlation_heatmap(df):

    numeric_df = df.select_dtypes(
        include=["int64", "float64"]
    )

    plt.figure(figsize=(10, 6))

    sns.heatmap(
        numeric_df.corr(),
        annot=True,
        cmap="coolwarm",
        linewidths=0.5
    )

    plt.title(
        "Weather Data Correlation Heatmap",
        fontsize=16,
        fontweight="bold"
    )

    plt.tight_layout()

    plt.savefig(
        "outputs/charts/correlation_heatmap.png",
        dpi=300
    )

    plt.close()


# ---------------------------------------------------
# FEATURE IMPORTANCE CHART
# ---------------------------------------------------

def feature_importance_chart(model, feature_names):

    importance = model.feature_importances_

    feature_df = pd.DataFrame({

        "Feature": feature_names,
        "Importance": importance

    })

    feature_df = feature_df.sort_values(
        by="Importance",
        ascending=False
    )

    plt.figure(figsize=(10, 5))

    sns.barplot(
        x="Importance",
        y="Feature",
        data=feature_df
    )

    plt.title(
        "ML Feature Importance",
        fontsize=16,
        fontweight="bold"
    )

    plt.xlabel("Importance Score", fontsize=12)

    plt.ylabel("Features", fontsize=12)

    plt.tight_layout()

    plt.savefig(
        "outputs/charts/feature_importance.png",
        dpi=300
    )

    plt.close()


# ---------------------------------------------------
# GENERATE ALL CHARTS TOGETHER
# ---------------------------------------------------

def generate_all_charts(df, model):

    feature_names = [
        "Temperature",
        "Humidity",
        "WindSpeed",
        "RainProbability",
        "Pressure"
    ]

    temperature_chart(df)

    humidity_chart(df)

    risk_distribution(df)

    correlation_heatmap(df)

    feature_importance_chart(
        model,
        feature_names
    )

    print("\n📊 All Charts Generated Successfully")

    print("📁 Saved inside outputs/charts/")