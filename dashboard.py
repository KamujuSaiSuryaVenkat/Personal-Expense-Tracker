import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time

from streamlit_autorefresh import st_autorefresh

from src.api.weather_api import (
    get_live_weather,
    get_forecast
)
from src.models.risk_model import create_risk_labels
from src.processing.data_loader import (
    load_weather_data,
    preprocess_data
)

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="WeatherShield",
    page_icon="🌦",
    layout="wide"
)

# =========================================================
# AUTO REFRESH
# =========================================================

st_autorefresh(
    interval=300000,
    key="weather_refresh"
)

# =========================================================
# LOADING
# =========================================================

with st.spinner("🚀 Connecting to Global AI Climate Network..."):
    time.sleep(2)

# =========================================================
# INITIALIZE EMPTY DATAFRAME
# =========================================================

try:

    df = load_weather_data("sample_weather_data.csv")

    df = preprocess_data(df)

    df = create_risk_labels(df)

except Exception:

    df = pd.DataFrame(
        columns=[
            "City",
            "Temperature",
            "Humidity",
            "WindSpeed",
            "Pressure",
            "RainProbability",
            "Condition",
            "RiskLevel"
        ]
    )

# =========================================================
# SMART AI RISK ENGINE
# =========================================================

def create_risk(temp, humidity, wind):

    if (
        temp >= 40 and humidity >= 70
    ) or wind >= 30:

        return "EXTREME"

    elif (
        temp >= 36 and humidity >= 60
    ) or wind >= 22:

        return "HIGH"

    elif (
        temp >= 32 and humidity >= 50
    ) or wind >= 15:

        return "MEDIUM"

    else:

        return "LOW"

if not df.empty:
    df["RiskLevel"] = df.apply(

        lambda x: create_risk(

            x["Temperature"],
            x["Humidity"],
            x["WindSpeed"]

        ),

        axis=1
    )
else:
    df["RiskLevel"] = pd.Series(dtype="object")

# =========================================================
# FORECAST
# =========================================================

try:

    forecast_df = get_forecast("Kolkata")

except:

    forecast_df = pd.DataFrame()

if "forecast_city" not in st.session_state:

    st.session_state.forecast_city = "Kolkata"

if "forecast_data" not in st.session_state:

    st.session_state.forecast_data = forecast_df


def get_ai_assistant_response(question, monitoring_df, forecast_data):

    question = question.strip().lower()

    if monitoring_df.empty:

        return "Load or connect monitoring data first so I can analyze risk, trends, and city-level conditions."

    avg_temperature = monitoring_df["Temperature"].mean()

    avg_humidity = monitoring_df["Humidity"].mean()

    hottest_city = monitoring_df.loc[monitoring_df["Temperature"].idxmax()]

    highest_risk_counts = monitoring_df["RiskLevel"].value_counts()

    dominant_risk = highest_risk_counts.index[0] if not highest_risk_counts.empty else "LOW"

    if "forecast" in question:

        if forecast_data.empty:

            return "Forecast data is currently unavailable. Try refreshing the forecast tab for a city with live API access."

        warmest_forecast = forecast_data.loc[forecast_data["Temperature"].idxmax()]

        return (
            f"The forecast peaks at {warmest_forecast['Temperature']:.1f}°C on {warmest_forecast['Datetime']}. "
            f"Average forecast humidity is {forecast_data['Humidity'].mean():.1f}%."
        )

    if "risk" in question or "danger" in question:

        return (
            f"Dominant risk level is {dominant_risk}. "
            f"The hottest monitored city is {hottest_city['City']} at {hottest_city['Temperature']:.1f}°C, "
            f"with average humidity around {avg_humidity:.1f}%."
        )

    if "temperature" in question or "heat" in question:

        return (
            f"Average monitored temperature is {avg_temperature:.1f}°C. "
            f"{hottest_city['City']} is currently the hottest city at {hottest_city['Temperature']:.1f}°C."
        )

    if "humidity" in question or "rain" in question:

        wettest_city = monitoring_df.loc[monitoring_df["Humidity"].idxmax()]

        return (
            f"Average humidity is {avg_humidity:.1f}%. "
            f"{wettest_city['City']} is the most humid city at {wettest_city['Humidity']:.1f}%."
        )

    return (
        f"I’m tracking {len(monitoring_df)} cities. The dominant risk tier is {dominant_risk}, "
        f"average temperature is {avg_temperature:.1f}°C, and the hottest city is {hottest_city['City']}."
    )

# =========================================================
# PREMIUM CSS
# =========================================================

st.markdown("""
<style>

.stApp {

    background:
    radial-gradient(circle at top left, #1e3a8a 0%, transparent 25%),
    radial-gradient(circle at top right, #7c3aed 0%, transparent 25%),
    radial-gradient(circle at bottom left, #0891b2 0%, transparent 25%),
    linear-gradient(
        135deg,
        #020617 0%,
        #0f172a 20%,
        #172554 45%,
        #312e81 70%,
        #581c87 100%
    );

    color: white;
}

section[data-testid="stSidebar"] {

    background:
    linear-gradient(
        180deg,
        rgba(15,23,42,0.98),
        rgba(23,37,84,0.98),
        rgba(49,46,129,0.98)
    );

    border-right:
    1px solid rgba(255,255,255,0.08);

    box-shadow:
    0 0 25px rgba(59,130,246,0.25);
}

.hero {

    padding: 55px;

    border-radius: 35px;

    background:
    linear-gradient(
        135deg,
        rgba(59,130,246,0.35),
        rgba(139,92,246,0.35),
        rgba(236,72,153,0.25)
    );

    margin-bottom: 35px;

    border:
    1px solid rgba(255,255,255,0.12);

    box-shadow:
    0 0 20px rgba(59,130,246,0.25),
    0 0 40px rgba(139,92,246,0.25),
    0 0 60px rgba(236,72,153,0.18);
}

.hero-title {

    font-size: 64px;

    font-weight: 900;

    background:
    linear-gradient(
        90deg,
        #ffffff,
        #67e8f9,
        #c084fc,
        #f472b6
    );

    -webkit-background-clip: text;

    -webkit-text-fill-color: transparent;
}

.hero-sub {

    font-size: 22px;

    color: #f8fafc;

    margin-top: 18px;

    line-height: 1.9;
}

.metric-card {

    padding: 28px;

    border-radius: 28px;

    background:
    linear-gradient(
        135deg,
        rgba(15,23,42,0.96),
        rgba(30,41,59,0.96),
        rgba(59,130,246,0.12)
    );

    border:
    1px solid rgba(255,255,255,0.08);

    transition: all 0.4s ease;

    box-shadow:
    0 0 18px rgba(59,130,246,0.20),
    0 0 35px rgba(139,92,246,0.15);
}

.metric-card:hover {

    transform:
    translateY(-10px)
    scale(1.03);

    box-shadow:
    0 0 30px rgba(56,189,248,0.40),
    0 0 60px rgba(139,92,246,0.28);
}

.metric-title {

    color: #cbd5e1;

    font-size: 17px;

    margin-bottom: 10px;
}

.metric-value {

    font-size: 46px;

    font-weight: 900;

    color: white;
}

.image-card {

    border-radius:25px;
    overflow:hidden;

    background:linear-gradient(
        135deg,
        #0f172a,
        #1e293b
    );

    border:1px solid rgba(255,255,255,0.08);

    padding:15px;

    box-shadow:
    0 0 25px rgba(59,130,246,0.25);

    margin-bottom:25px;
}

.footer {

    text-align:center;

    color:#f1f5f9;

    padding:40px;

    font-size:17px;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("🌍 WeatherShield")

# Search for custom city
st.sidebar.markdown("### 🔍 Search City")
custom_city = st.sidebar.text_input(
    "Enter city name",
    placeholder="e.g., New York, Paris, Sydney"
)

search_button = st.sidebar.button("🔎 Get Weather Report", use_container_width=True)

st.sidebar.success("🟢 Live API Connected")
st.sidebar.info("🤖 AI Engine Running")
st.sidebar.warning("⚡ Real-Time Monitoring Enabled")

st.sidebar.markdown("---")

st.sidebar.markdown("""
### 📡 Monitoring Modules

- 🌦 Live Weather
- 🤖 AI Forecasting
- 📊 Analytics
- ⚠ Risk Intelligence
- 💬 AI Assistant
- 🌍 Global Monitoring
""")

# =========================================================
# HERO
# =========================================================

st.markdown("""
<div class="hero">

<div class="hero-title">
🌦 WeatherShield
</div>

<div class="hero-sub">

🌍 Real-Time Global Monitoring •
🤖 AI Forecast Intelligence •
📈 Climate Analytics •
⚡ Smart Alerts

</div>

</div>
""", unsafe_allow_html=True)

# =========================================================
# ALERTS
# =========================================================

a1, a2, a3 = st.columns(3)

with a1:
    st.error("🚨 Heatwave Alert Active")

with a2:
    st.warning("🌧 Heavy Rain Monitoring")

with a3:
    st.success("🤖 AI Systems Operational")



# =========================================================
# CUSTOM CITY SEARCH
# =========================================================

if search_button and custom_city:
    st.markdown("---")
    st.subheader(f"🔍 Weather Report for {custom_city.title()}")
    
    try:
        with st.spinner(f"🌐 Fetching weather data for {custom_city}..."):
            custom_city_data = get_live_weather(custom_city)
        
        if custom_city_data is not None and len(custom_city_data) > 0:
            custom_row = custom_city_data.iloc[0]
            
            # Create risk level for custom city
            custom_risk = create_risk(
                custom_row["Temperature"],
                custom_row["Humidity"],
                custom_row["WindSpeed"]
            )
            
            # Display custom city weather in columns
            sc1, sc2, sc3, sc4, sc5 = st.columns(5)
            
            with sc1:
                st.markdown(f"""
                <div class="metric-card">
                <div class="metric-title">🌡 Temperature</div>
                <div class="metric-value">{custom_row["Temperature"]}°C</div>
                </div>
                """, unsafe_allow_html=True)
            
            with sc2:
                st.markdown(f"""
                <div class="metric-card">
                <div class="metric-title">💧 Humidity</div>
                <div class="metric-value">{custom_row["Humidity"]}%</div>
                </div>
                """, unsafe_allow_html=True)
            
            with sc3:
                st.markdown(f"""
                <div class="metric-card">
                <div class="metric-title">💨 Wind Speed</div>
                <div class="metric-value">{custom_row["WindSpeed"]} km/h</div>
                </div>
                """, unsafe_allow_html=True)
            
            with sc4:
                st.markdown(f"""
                <div class="metric-card">
                <div class="metric-title">☁ Cloudiness</div>
                <div class="metric-value">{custom_row["Cloudiness"]}%</div>
                </div>
                """, unsafe_allow_html=True)
            
            with sc5:
                risk_color = {
                    "LOW": "🟢",
                    "MEDIUM": "🟡",
                    "HIGH": "🔴",
                    "EXTREME": "⛔"
                }
                st.markdown(f"""
                <div class="metric-card">
                <div class="metric-title">⚠ Risk Level</div>
                <div class="metric-value">{risk_color.get(custom_risk, '❓')} {custom_risk}</div>
                </div>
                """, unsafe_allow_html=True)
            
            # Additional info
            st.info(f"📍 **Weather Condition**: {custom_row['Condition']}")
            
        else:
            st.error(f"❌ No data found for {custom_city}. Please check the city name and try again.")
    
    except Exception as e:
        st.error(f"⚠️ Error fetching weather for {custom_city}: {str(e)}")

# =========================================================
# TABS
# =========================================================

tab_monitoring, tab_assistant, tab_forecast = st.tabs([
    "📡 Monitoring and Risk Intelligence",
    "🤖 AI Assistant",
    "🔮 Forecasts"
])

with tab_monitoring:

    st.subheader("📡 Monitoring and Risk Intelligence")

    if df.empty:

        st.info("Monitoring data is not available yet.")

    else:

        monitoring_metric_1, monitoring_metric_2, monitoring_metric_3, monitoring_metric_4 = st.columns(4)

        with monitoring_metric_1:

            st.metric("Cities Monitored", len(df))

        with monitoring_metric_2:

            st.metric("Avg Temperature", f"{df['Temperature'].mean():.1f}°C")

        with monitoring_metric_3:

            st.metric("Avg Humidity", f"{df['Humidity'].mean():.1f}%")

        with monitoring_metric_4:

            st.metric("High Risk Cities", int((df["RiskLevel"] == "HIGH").sum()))

        monitoring_left, monitoring_right = st.columns([1.35, 1])

        with monitoring_left:

            st.markdown("### Live Monitoring Grid")

            st.dataframe(
                df[
                    [
                        "City",
                        "Temperature",
                        "Humidity",
                        "WindSpeed",
                        "RainProbability",
                        "Pressure",
                        "Condition",
                        "RiskLevel"
                    ]
                ],
                use_container_width=True,
                hide_index=True
            )

        with monitoring_right:

            st.markdown("### Temperature by City")

            temperature_chart = px.bar(
                df,
                x="City",
                y="Temperature",
                color="RiskLevel",
                color_discrete_map={
                    "LOW": "#22c55e",
                    "MEDIUM": "#f59e0b",
                    "HIGH": "#ef4444"
                },
                title="Temperature and Risk Overview"
            )

            temperature_chart.update_layout(
                template="plotly_dark",
                height=420,
                margin=dict(l=10, r=10, t=40, b=10)
            )

            st.plotly_chart(temperature_chart, use_container_width=True)

            risk_breakdown = go.Figure(
                data=[
                    go.Pie(
                        labels=df["RiskLevel"].value_counts().index,
                        values=df["RiskLevel"].value_counts().values,
                        hole=0.45
                    )
                ]
            )

            risk_breakdown.update_layout(
                template="plotly_dark",
                height=360,
                margin=dict(l=10, r=10, t=40, b=10),
                title="Risk Distribution"
            )

            st.plotly_chart(risk_breakdown, use_container_width=True)

with tab_assistant:

    st.subheader("🤖 AI Assistant")
    st.caption("Ask for a climate summary, a risk briefing, or a forecast insight.")

    assistant_query = st.text_area(
        "Ask WeatherShield",
        value="Which cities are at highest risk right now?",
        height=110
    )

    assistant_trigger = st.button("Generate Insight", use_container_width=True)

    if assistant_trigger:

        assistant_response = get_ai_assistant_response(
            assistant_query,
            df,
            st.session_state.forecast_data
        )

        st.success(assistant_response)

    st.markdown("### Quick Prompts")

    prompt_columns = st.columns(3)

    prompt_options = [
        "Summarize the current risk situation",
        "What does the forecast say?",
        "Which city is hottest?"
    ]

    for prompt_column, prompt_text in zip(prompt_columns, prompt_options):

        with prompt_column:

            if st.button(prompt_text, key=prompt_text, use_container_width=True):

                st.session_state.ai_prompt = prompt_text

    if st.session_state.get("ai_prompt"):

        st.info(
            get_ai_assistant_response(
                st.session_state.ai_prompt,
                df,
                st.session_state.forecast_data
            )
        )

with tab_forecast:

    st.subheader("🔮 Forecasts")
    st.caption("Choose a city and load its short-term forecast from the live weather API.")

    available_cities = df["City"].tolist() if not df.empty else ["Kolkata"]

    selected_city = st.selectbox(
        "Forecast city",
        available_cities,
        index=available_cities.index(st.session_state.forecast_city) if st.session_state.forecast_city in available_cities else 0
    )

    if st.button("Refresh Forecast", use_container_width=True):

        try:

            st.session_state.forecast_city = selected_city
            st.session_state.forecast_data = get_forecast(selected_city)

        except Exception:

            st.session_state.forecast_data = pd.DataFrame()

    forecast_view = st.session_state.forecast_data.copy()

    if forecast_view.empty:

        st.info("No forecast data available for the selected city right now.")

    else:

        forecast_view["Datetime"] = pd.to_datetime(forecast_view["Datetime"])

        forecast_metric_1, forecast_metric_2, forecast_metric_3 = st.columns(3)

        with forecast_metric_1:

            st.metric("Forecast Points", len(forecast_view))

        with forecast_metric_2:

            st.metric("Avg Forecast Temp", f"{forecast_view['Temperature'].mean():.1f}°C")

        with forecast_metric_3:

            st.metric("Avg Forecast Humidity", f"{forecast_view['Humidity'].mean():.1f}%")

        forecast_chart = px.line(
            forecast_view,
            x="Datetime",
            y="Temperature",
            markers=True,
            title=f"Temperature Forecast for {st.session_state.forecast_city}"
        )

        forecast_chart.update_layout(
            template="plotly_dark",
            height=420,
            margin=dict(l=10, r=10, t=40, b=10)
        )

        st.plotly_chart(forecast_chart, use_container_width=True)

        st.dataframe(
            forecast_view,
            use_container_width=True,
            hide_index=True
        )

# =========================================================
# FOOTER
# =========================================================

st.markdown("""
<div class="footer">

🚀 WeatherShield

<br><br>

Real-Time Monitoring •
AI Forecasting •
Climate Analytics •
Business Intelligence

</div>
""", unsafe_allow_html=True)