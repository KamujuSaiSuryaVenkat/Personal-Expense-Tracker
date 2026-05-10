from src.processing.data_loader import (
    load_weather_data,
    preprocess_data
)

from src.models.risk_model import (
    create_risk_labels,
    train_model
)

from src.visualization.charts import (
    generate_all_charts
)


def main():

    print("\n" + "=" * 60)

    print("🌦 WEATHER FORECAST & RISK ANALYSIS SYSTEM")

    print("=" * 60)

    # ---------------------------------------------------
    # LOAD DATA
    # ---------------------------------------------------

    print("\n📥 Loading Weather Dataset...")

    df = load_weather_data(
        "sample_weather_data.csv"
    )

    print("✅ Dataset Loaded Successfully")

    # ---------------------------------------------------
    # PREPROCESS DATA
    # ---------------------------------------------------

    print("\n🧹 Cleaning Dataset...")

    df = preprocess_data(df)

    print("✅ Data Preprocessing Completed")

    # ---------------------------------------------------
    # CREATE RISK LABELS
    # ---------------------------------------------------

    print("\n⚠ Generating Weather Risk Levels...")

    df = create_risk_labels(df)

    print("✅ Risk Labels Added Successfully")

    # ---------------------------------------------------
    # DISPLAY DATA
    # ---------------------------------------------------

    print("\n📊 WEATHER DATA\n")

    print(df)

    # ---------------------------------------------------
    # TRAIN MODEL
    # ---------------------------------------------------

    print("\n🤖 Training Machine Learning Model...")

    model, accuracy, report = train_model(df)

    print("✅ Model Training Completed")

    # ---------------------------------------------------
    # MODEL RESULTS
    # ---------------------------------------------------

    print("\n📈 MODEL PERFORMANCE")

    print(f"\n✅ Accuracy Score: {accuracy:.2f}")

    print("\n📋 Classification Report:\n")

    print(report)

    # ---------------------------------------------------
    # GENERATE CHARTS
    # ---------------------------------------------------

    print("\n📊 Generating Visualization Charts...")

    generate_all_charts(df, model)

    # ---------------------------------------------------
    # FINAL MESSAGE
    # ---------------------------------------------------

    print("\n" + "=" * 60)

    print("🚀 WEATHER ANALYTICS SYSTEM EXECUTED SUCCESSFULLY")

    print("=" * 60)

    print("\n📁 Check Generated Files:")

    print("   ➜ outputs/charts/")

    print("\n🔥 Your WOW-Level Project Is Growing Successfully")


if __name__ == "__main__":
    main()