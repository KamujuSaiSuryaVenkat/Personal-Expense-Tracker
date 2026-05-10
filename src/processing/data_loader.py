import pandas as pd


def load_weather_data(file_path):

    df = pd.read_csv(file_path)

    return df


def preprocess_data(df):

    # Remove duplicate rows
    df = df.drop_duplicates()

    # Fill missing values
    df = df.fillna(0)

    # Standardize city names
    df["City"] = df["City"].str.title()

    return df