
import sys
from pathlib import Path

CURRENT_DIR = Path(__file__).resolve().parent

# Add streamlit folder to python path
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))


import streamlit as st

from streamlit_folium import st_folium

from utils.india_folium_map import create_india_map
from utils.india_map import STATE_CITY_MAP

import streamlit as st
import pandas as pd
import plotly.express as px
import joblib
import requests
from datetime import datetime, timedelta, timezone

def clean_html(html_str: str) -> str:
    """Strips leading and trailing whitespace from every line of HTML to prevent Markdown code block formatting bugs."""
    return "\n".join(line.strip() for line in html_str.splitlines())




ROOT = Path(__file__).resolve().parents[1]

# Dataset for Dashboard & Analytics
ROOT = Path(__file__).resolve().parents[1]

# -------------------------
# Dataset
# -------------------------

VISUAL_DATASET = ROOT / "dataset" / "weather.csv"
df = pd.read_csv(VISUAL_DATASET)

# Convert Date column
df["Date"] = pd.to_datetime(
    df["Date"],
    dayfirst=True,
    errors="coerce"
)

df = df.dropna(subset=["Date"])

df["Year"] = df["Date"].dt.year
df["Month"] = df["Date"].dt.month
df["Day"] = df["Date"].dt.day
df["Hour"] = df["Date"].dt.hour
df["DayOfWeek"] = df["Date"].dt.day_name()
# -------------------------
# ML Model
# -------------------------

MODEL = ROOT / "models" / "weather_model.pkl"

model = joblib.load(MODEL)



le_city = joblib.load(ROOT / "models" / "le_city.pkl")
le_weather = joblib.load(ROOT / "models" / "le_weather.pkl")
le_day = joblib.load(ROOT / "models" / "le_day.pkl")
le_season = joblib.load(ROOT / "models" / "le_season.pkl")
API_KEY = "1becb0fb56249486d02f3d4f89203315"
import requests

def get_live_weather(city):

    url = "https://api.openweathermap.org/data/2.5/weather"

    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json()

    return None


def get_forecast(city):
    url = "https://api.openweathermap.org/data/2.5/forecast"

    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json()

    return None


DEFAULT_STATE = "Karnataka"
DEFAULT_CITY = "Bengaluru"

CITY_MODEL_FALLBACK = {
    "Bangalore": "Bengaluru",
    "Visakhapatnam": "Hyderabad", "Vijayawada": "Hyderabad", "Tirupati": "Bengaluru",
    "Itanagar": "Hyderabad", "Tawang": "Hyderabad", "Pasighat": "Hyderabad",
    "Guwahati": "Hyderabad", "Dibrugarh": "Hyderabad", "Silchar": "Hyderabad",
    "Patna": "New_Delhi", "Gaya": "New_Delhi", "Muzaffarpur": "New_Delhi",
    "Raipur": "Ahmedabad", "Bhilai": "Ahmedabad", "Bilaspur": "Ahmedabad",
    "Surat": "Ahmedabad", "Vadodara": "Ahmedabad",
    "Gurugram": "New_Delhi", "Faridabad": "New_Delhi", "Ambala": "New_Delhi",
    "Shimla": "New_Delhi", "Manali": "New_Delhi", "Dharamshala": "New_Delhi",
    "Ranchi": "Hyderabad", "Jamshedpur": "Hyderabad", "Dhanbad": "Hyderabad",
    "Thiruvananthapuram": "Kochi", "Kozhikode": "Kochi",
    "Indore": "Ahmedabad", "Gwalior": "Ahmedabad",
    "Nagpur": "Pune", "Nashik": "Mumbai",
    "Imphal": "Hyderabad", "Churachandpur": "Hyderabad", "Thoubal": "Hyderabad",
    "Shillong": "Hyderabad", "Tura": "Hyderabad", "Jowai": "Hyderabad",
    "Aizawl": "Hyderabad", "Lunglei": "Hyderabad", "Champhai": "Hyderabad",
    "Kohima": "Hyderabad", "Dimapur": "Hyderabad", "Mokokchung": "Hyderabad",
    "Bhubaneswar": "Hyderabad", "Cuttack": "Hyderabad", "Puri": "Hyderabad",
    "Amritsar": "New_Delhi", "Ludhiana": "New_Delhi", "Jalandhar": "New_Delhi",
    "Udaipur": "Jaipur", "Jodhpur": "Jaipur",
    "Gangtok": "Hyderabad", "Namchi": "Hyderabad", "Pelling": "Hyderabad",
    "Coimbatore": "Bengaluru", "Madurai": "Bengaluru",
    "Warangal": "Hyderabad", "Nizamabad": "Hyderabad",
    "Agartala": "Hyderabad", "Dharmanagar": "Hyderabad",
    "Varanasi": "New_Delhi", "Agra": "New_Delhi", "Kanpur": "New_Delhi",
    "Dehradun": "New_Delhi", "Haridwar": "New_Delhi", "Nainital": "New_Delhi",
    "Siliguri": "Hyderabad", "Durgapur": "Hyderabad",
    "New Delhi": "New_Delhi", "Dwarka": "New_Delhi", "Delhi": "New_Delhi",
    "Srinagar": "New_Delhi", "Jammu": "New_Delhi", "Anantnag": "New_Delhi",
    "Leh": "New_Delhi", "Kargil": "New_Delhi",
    "Port Blair": "Bengaluru", "Havelock": "Bengaluru",
    "Chandigarh": "New_Delhi",
    "Daman": "Ahmedabad", "Diu": "Ahmedabad", "Silvassa": "Mumbai",
    "Kavaratti": "Kochi", "Agatti": "Kochi",
    "Puducherry": "Bengaluru", "Karaikal": "Bengaluru",
    "Panaji": "Mumbai", "Margao": "Mumbai"
}


def safe_encode_city(city_name):
    classes = list(le_city.classes_)
    if city_name in classes:
        return le_city.transform([city_name])[0]
    
    fallback = CITY_MODEL_FALLBACK.get(city_name)
    if fallback and fallback in classes:
        return le_city.transform([fallback])[0]
    
    clean_name = city_name.replace(" ", "_")
    if clean_name in classes:
        return le_city.transform([clean_name])[0]

    mapping = {
        "Bangalore": "Bengaluru",
        "New Delhi": "New_Delhi",
        "Delhi": "New_Delhi",
        "Chennai": "Bengaluru",
        "Kolkata": "Hyderabad",
        "Lucknow": "New_Delhi",
        "Bhopal": "Ahmedabad",
        "Goa": "Mumbai"
    }
    mapped = mapping.get(city_name)
    if mapped and mapped in classes:
        return le_city.transform([mapped])[0]

    default_c = "Bengaluru" if "Bengaluru" in classes else classes[0]
    return le_city.transform([default_c])[0]


def safe_encode_weather(weather_name):
    classes = list(le_weather.classes_)
    if weather_name in classes:
        return le_weather.transform([weather_name])[0]
    
    weather_map = {
        "Clouds": "Cloudy",
        "Drizzle": "Rain",
        "Mist": "Cloudy",
        "Haze": "Cloudy",
        "Fog": "Cloudy",
        "Smoke": "Cloudy",
        "Snow": "Rain",
        "Clear": "Clear",
        "Thunderstorm": "Thunderstorm"
    }
    mapped = weather_map.get(weather_name, "Clear")
    if mapped not in classes:
        mapped = classes[0]
    return le_weather.transform([mapped])[0]


def safe_encode_day(day_name):
    classes = list(le_day.classes_)
    if day_name in classes:
        return le_day.transform([day_name])[0]
    return le_day.transform([classes[0]])[0]


def safe_encode_season(season_name):
    classes = list(le_season.classes_)
    if season_name in classes:
        return le_season.transform([season_name])[0]
    return le_season.transform([classes[0]])[0]



def get_next_hours_forecast(forecast_data, count=3):
    entries = forecast_data.get("list", []) if forecast_data else []
    tz_offset = forecast_data.get("city", {}).get("timezone", 0) if forecast_data else 0
    tz = timezone(timedelta(seconds=tz_offset)) if tz_offset else None
    slots = []

    for item in entries[:count]:
        if tz:
            timestamp = datetime.fromtimestamp(item["dt"], tz=timezone.utc).astimezone(tz)
        else:
            timestamp = datetime.fromtimestamp(item["dt"])

        main = item.get("main", {})
        weather = item.get("weather", [{}])[0]
        rain = item.get("rain", {}).get("3h", 0)
        slots.append({
            "time": timestamp.strftime("%I %p"),
            "temp": main.get("temp", 0),
            "icon": weather.get("icon", "01d"),
            "description": weather.get("description", "Clear"),
            "rain": rain,
        })

    return slots


def get_tomorrow_summary(forecast_data):
    entries = forecast_data.get("list", []) if forecast_data else []
    if not entries:
        return None

    tz_offset = forecast_data.get("city", {}).get("timezone", 0) if forecast_data else 0
    tz = timezone(timedelta(seconds=tz_offset)) if tz_offset else None

    if tz:
        now_city = datetime.now(timezone.utc).astimezone(tz)
    else:
        now_city = datetime.now()

    tomorrow_date = (now_city + timedelta(days=1)).date()

    items = []
    for item in entries:
        if tz:
            item_date = datetime.fromtimestamp(item["dt"], tz=timezone.utc).astimezone(tz).date()
        else:
            item_date = datetime.fromtimestamp(item["dt"]).date()
        if item_date == tomorrow_date:
            items.append(item)

    if not items:
        items = entries[:8]

    temps = [item.get("main", {}).get("temp", 0) for item in items]
    rain_total = sum(item.get("rain", {}).get("3h", 0) for item in items)
    wind_speed = max((item.get("wind", {}).get("speed", 0) for item in items), default=0)

    return {
        "max_temp": max(temps) if temps else 0,
        "min_temp": min(temps) if temps else 0,
        "rain": rain_total,
        "wind": wind_speed,
    }


def get_season(month):

    if month in [12,1,2]:
        return "Winter"

    elif month in [3,4,5]:
        return "Summer"

    elif month in [6,7,8]:
        return "Monsoon"

    return "Autumn"
# ----------------------------
# Page Configuration & Styling
# ----------------------------
st.set_page_config(
    page_title="Weather Prediction Dashboard",
    page_icon="🌦️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load CSS stylesheet
def load_css():
    css_path = Path(__file__).parent / "style.css"
    if css_path.exists():
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# Plotly styling helper
def style_plotly_chart(fig):
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_family="Inter, sans-serif",
        font_color="#E2E8F0",
        title_font=dict(size=16, family="Outfit, sans-serif", color="#FFFFFF"),
        margin=dict(l=40, r=20, t=50, b=40),
        legend=dict(
            bgcolor="rgba(15, 23, 42, 0.6)",
            bordercolor="rgba(255, 255, 255, 0.08)",
            borderwidth=1
        )
    )
    fig.update_xaxes(
        gridcolor="rgba(255, 255, 255, 0.05)",
        linecolor="rgba(255, 255, 255, 0.1)",
        title_font=dict(size=12, color="#94A3B8")
    )
    fig.update_yaxes(
        gridcolor="rgba(255, 255, 255, 0.05)",
        linecolor="rgba(255, 255, 255, 0.1)",
        title_font=dict(size=12, color="#94A3B8")
    )
    return fig

# Custom KPI Card Renderer
def render_kpi_card(label, value, icon, target_num=None, suffix="", card_id=""):
    html_content = f"""
    <div class="kpi-card" id="card-{card_id}">
        <div class="kpi-icon-container">
            <span class="kpi-icon">{icon}</span>
        </div>
        <div class="kpi-details">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value" id="kpi-val-{card_id}">{value}</div>
        </div>
    </div>
    """
    st.markdown(html_content, unsafe_allow_html=True)

# Custom HTML Table Renderer
def render_html_table(df_to_show):
    table_html = df_to_show.to_html(classes="custom-table", index=False, border=0)
    st.markdown(f'<div class="table-container">{table_html}</div>', unsafe_allow_html=True)


# ----------------------------
# Sidebar Header
# ----------------------------
st.sidebar.markdown("""
<div class="sidebar-title">🌦 Weather Prediction</div>
<div class="sidebar-subtitle">Machine Learning Dashboard <span style="background: rgba(37,99,235,0.2); color: #38BDF8; padding: 2px 6px; border-radius: 4px; font-size: 0.75rem; margin-left: 5px;">v1.0</span></div>
""", unsafe_allow_html=True)

# ----------------------------
# Sidebar Navigation
# ----------------------------
page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Dashboard",
        "📂 Dataset",
        "📊 Analytics",
        "🌍 Live Weather",
        "🤖 Prediction",
        "📄 Reports",
        "ℹ About"
    ]
)

# ============================================
# DASHBOARD
# ============================================

if page == "🏠 Dashboard":

    st.markdown("""
    <div class="hero-banner">
        <div class="hero-header">
            <span class="hero-icon">🌦️</span>
            <div class="hero-title-group">
                <h1 class="hero-title">Weather Prediction Dashboard</h1>
                <h3 class="hero-subtitle">Principle of Data Science Project</h3>
            </div>
        </div>
        <div class="hero-badges">
            <span class="hero-badge">🤖 Machine Learning</span>
            <span class="hero-badge">🌍 OpenWeather API</span>
            <span class="hero-badge">🌲 Random Forest</span>
            <span class="hero-badge">📊 Real-Time Analytics</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        render_kpi_card("Total Records", f"{len(df)}", "📊", len(df), "", "records")

    with col2:
        render_kpi_card("Cities", f"{df['City'].nunique()}", "🏙", df["City"].nunique(), "", "cities")

    with col3:
        avg_temp = float(df['Temperature'].mean())
        render_kpi_card("Avg Temperature", f"{avg_temp:.2f}°C", "🌡", avg_temp, "°C", "temp")

    with col4:
        render_kpi_card("Weather Types", f"{df['Weather'].nunique()}", "☁", df["Weather"].nunique(), "", "weather")

    st.divider()

    left, right = st.columns(2)

    with left:
        fig = px.histogram(
            df,
            x="Temperature",
            nbins=30,
            title="Temperature Distribution",
            color_discrete_sequence=["#2563EB"]
        )
        style_plotly_chart(fig)
        st.plotly_chart(fig, use_container_width=True)

    with right:
        fig = px.pie(
            df,
            names="Weather",
            title="Weather Distribution",
            color_discrete_sequence=px.colors.qualitative.Safe
        )
        style_plotly_chart(fig)
        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    st.subheader("Recent Dataset")

    # Search & Pagination inside Dashboard Recent Dataset Table
    search_col1, search_col2 = st.columns([3, 1])
    with search_col1:
        search_query = st.text_input("🔍 Search by City or Weather", placeholder="Type city or weather to filter...", key="dash_search")
    
    # Filter
    filtered_dash_df = df
    if search_query:
        filtered_dash_df = df[
            df["City"].str.contains(search_query, case=False, na=False) |
            df["Weather"].str.contains(search_query, case=False, na=False)
        ]
        
    with search_col2:
        items_per_page = 10
        total_items = len(filtered_dash_df)
        total_pages = max(1, (total_items + items_per_page - 1) // items_per_page)
        page_num = st.number_input("Page", min_value=1, max_value=total_pages, value=1, step=1, key="dash_page")
        
    start_idx = (page_num - 1) * items_per_page
    end_idx = start_idx + items_per_page
    page_df = filtered_dash_df.iloc[start_idx:end_idx]
    
    
    render_html_table(
        page_df[
            [
                "Date",
                "City",
                "Temperature",
                "Humidity",
                "Pressure",
                "Wind_Speed",
                "Cloud_Cover",
                "Rainfall",
                "Weather"
            ]
        ]
    )
# ============================================
# DATASET PAGE
# ============================================

elif page == "📂 Dataset":

    st.title("📂 Weather Dataset Explorer")
    st.markdown("### Search, filter, and analyze the dataset records")
    st.divider()

    # Search and Filter Cards
    col_filter1, col_filter2 = st.columns(2)
    with col_filter1:
        search_city = st.text_input("🏙 Search by City", placeholder="Type city name to search...", value="")
    with col_filter2:
        weather_options = ["All"] + list(df["Weather"].unique())
        filter_weather = st.selectbox("☁ Filter Weather Condition", options=weather_options, index=0)

    # Filter Dataframe
    filtered_df = df
    if search_city:
        filtered_df = filtered_df[filtered_df["City"].str.contains(search_city, case=False, na=False)]
    if filter_weather != "All":
        filtered_df = filtered_df[filtered_df["Weather"] == filter_weather]

    # Top Statistics KPI Cards for filtered data
    col_kpi1, col_kpi2, col_kpi3, col_kpi4 = st.columns(4)
    with col_kpi1:
        render_kpi_card("Filtered Records", f"{len(filtered_df)}", "📋", len(filtered_df), "", "filt_rec")
    with col_kpi2:
        filt_avg_temp = float(filtered_df["Temperature"].mean()) if len(filtered_df) > 0 else 0.0
        render_kpi_card("Avg Temp", f"{filt_avg_temp:.1f}°C", "🌡", filt_avg_temp, "°C", "filt_temp")
    with col_kpi3:
        filt_avg_hum = float(filtered_df["Humidity"].mean()) if len(filtered_df) > 0 else 0.0
        render_kpi_card("Avg Humidity", f"{filt_avg_hum:.1f}%", "💧", filt_avg_hum, "%", "filt_hum")
    with col_kpi4:
        filt_avg_wind = float(filtered_df["Wind_Speed"].mean()) if len(filtered_df) > 0 else 0.0
        render_kpi_card("Avg Wind", f"{filt_avg_wind:.1f} m/s", "🌬", filt_avg_wind, " m/s", "filt_wind")

    st.divider()

    # Download Button & Search results header
    col_hdr1, col_hdr2 = st.columns([3, 1])
    with col_hdr1:
        st.subheader("Dataset Preview")
    with col_hdr2:
        st.download_button(
            "⬇ Download CSV",
            filtered_df.to_csv(index=False),
            file_name="weather_dataset_filtered.csv",
            mime="text/csv"
        )

    # Display scrollable HTML table (limit to 100 rows for performance)
    items_to_show = 100
    if len(filtered_df) > items_to_show:
        st.caption(f"Showing top {items_to_show} of {len(filtered_df)} matching rows. Download CSV to view all.")
        display_df = filtered_df.head(items_to_show)
    else:
        st.caption(f"Showing all {len(filtered_df)} matching rows.")
        display_df = filtered_df

    # Render HTML table scrollable
    table_html = display_df.to_html(classes="custom-table", index=False, border=0)
    st.markdown(f'<div class="table-container" style="max-height: 400px; overflow-y: auto;">{table_html}</div>', unsafe_allow_html=True)

    st.divider()

    st.subheader("Dataset Statistics Summary")
    desc_df = filtered_df.describe().reset_index()
    desc_df.columns = ["Metric"] + list(filtered_df.describe().columns)
    
    # Format floating point numbers in describe table
    for col in desc_df.columns:
        if col != "Metric":
            desc_df[col] = desc_df[col].map(lambda x: f"{x:.2f}" if pd.notnull(x) else "")
            
    render_html_table(desc_df)

# ============================================
# ANALYTICS PAGE
# ============================================

elif page == "📊 Analytics":

    st.title("📊 Weather Analytics")
    st.markdown("### Deep-dive visual analysis of weather trends, metrics, and relationships")
    st.divider()

    tab_overview, tab_monthly, tab_weather, tab_correlation = st.tabs([
        "📈 Overview & Distributions", 
        "📅 Monthly Trends", 
        "🌦 Weather Conditions", 
        "🔗 Feature Correlation"
    ])

    with tab_overview:
        st.markdown("### Feature Distributions")
        # Row 1
        col1, col2 = st.columns(2)
        with col1:
            fig1 = px.histogram(
                df,
                x="Temperature",
                nbins=30,
                color="Weather",
                title="Temperature Distribution by Weather Condition",
                color_discrete_sequence=px.colors.qualitative.Safe
            )
            st.plotly_chart(style_plotly_chart(fig1), use_container_width=True)
        with col2:
            fig2 = px.histogram(
                df,
                x="Humidity",
                nbins=30,
                color="Weather",
                title="Humidity Distribution by Weather Condition",
                color_discrete_sequence=px.colors.qualitative.Safe
            )
            st.plotly_chart(style_plotly_chart(fig2), use_container_width=True)
            
        st.divider()
        
        # Row 2
        col3, col4 = st.columns(2)
        with col3:
            fig3 = px.box(
                df,
                y="Pressure",
                color="Weather",
                title="Pressure Analysis by Weather Condition",
                color_discrete_sequence=px.colors.qualitative.Safe
            )
            st.plotly_chart(style_plotly_chart(fig3), use_container_width=True)
        with col4:
            fig4 = px.box(
                df,
                y="Wind_Speed",
                color="Weather",
                title="Wind Speed Analysis by Weather Condition",
                color_discrete_sequence=px.colors.qualitative.Safe
            )
            st.plotly_chart(style_plotly_chart(fig4), use_container_width=True)

    with tab_monthly:
        st.markdown("### Monthly Weather Trends")
        monthly = df.groupby("Month")["Temperature"].mean().reset_index()
       
        fig5 = px.line(
            monthly,
            x="Month",
            y="Temperature",
            markers=True,
            title="Monthly Average Temperature Trend",
            color_discrete_sequence=["#06B6D4"]
        )
        st.plotly_chart(style_plotly_chart(fig5), use_container_width=True)
        
        st.divider()
        st.markdown("### Temperature vs. Humidity Relationship")
        fig_scatter = px.scatter(
            df,
            x="Temperature",
            y="Humidity",
            color="Weather",
            title="Scatter Plot: Temperature vs. Humidity",
            color_discrete_sequence=px.colors.qualitative.Safe,
            hover_data=["City", "Month"]
        )
        st.plotly_chart(style_plotly_chart(fig_scatter), use_container_width=True)

    with tab_weather:
        st.markdown("### Weather Condition Analysis")
        col5, col6 = st.columns(2)
        with col5:
            city_temp = df.groupby("City")["Temperature"].mean().reset_index()
            fig6 = px.bar(
                city_temp,
                x="City",
                y="Temperature",
                color="Temperature",
                title="Average Temperature by City",
                color_continuous_scale="Viridis"
            )
            st.plotly_chart(style_plotly_chart(fig6), use_container_width=True)
        with col6:
            weather_count = df["Weather"].value_counts().reset_index()
            weather_count.columns = ["Weather", "Count"]
            fig7 = px.pie(
                weather_count,
                names="Weather",
                values="Count",
                title="Weather Conditions Distribution",
                color_discrete_sequence=px.colors.qualitative.Safe
            )
            st.plotly_chart(style_plotly_chart(fig7), use_container_width=True)

    with tab_correlation:
        st.markdown("### Feature Correlation Heatmap")
        numeric_df = df.select_dtypes(include="number")
        corr = numeric_df.corr()
        fig8 = px.imshow(
            corr,
            text_auto=True,
            color_continuous_scale="RdBu_r",
            title="Feature Correlation Matrix"
        )
        st.plotly_chart(style_plotly_chart(fig8), use_container_width=True)
        
    st.success("Analytics Loaded Successfully ✅")

# ============================================
# LIVE WEATHER
# ============================================

elif page == "🌍 Live Weather":

    st.title("🌍 Live Weather Analytics")
    st.markdown(
        "### Pick a state and city to view live weather, AI predictions, and the next few hours"
    )
    st.divider()


    # -------------------------------
    # Location Session Handling
    # -------------------------------
    # Default values

    if "selected_state" not in st.session_state:
        st.session_state.selected_state = DEFAULT_STATE

    if "selected_city" not in st.session_state:
        st.session_state.selected_city = DEFAULT_CITY

    # Map Section Header
    st.markdown("## 🇮🇳 India Weather Map")
    st.caption("Click any state on the map to select state & city location")


    # Create Folium map passing currently selected state for visual highlighting
    india_map = create_india_map(selected_state=st.session_state.selected_state)

    map_data = st_folium(
        india_map,
        use_container_width=True,
        height=500,
        key="india_map"
    )

    # Detect clicked state from map interaction (with multi-layer fallback)
    if map_data:
        clicked_state = None

        # 1. Check last_active_drawing feature
        drawing = map_data.get("last_active_drawing")
        if drawing and isinstance(drawing, dict):
            properties = drawing.get("properties", {})
            clicked_state = (
                properties.get("NAME_1")
                or properties.get("state_name")
                or properties.get("ST_NM")
            )

        # 2. Fallback to last_object_clicked_tooltip
        if not clicked_state:
            tooltip = map_data.get("last_object_clicked_tooltip")
            if tooltip and isinstance(tooltip, str) and "State:" in tooltip:
                clicked_state = tooltip.replace("State:", "").strip()

        # 3. Fallback to last_object_clicked_popup
        if not clicked_state:
            popup = map_data.get("last_object_clicked_popup")
            if popup and isinstance(popup, str) and "State:" in popup:
                clicked_state = popup.replace("Selected State:", "").replace("State:", "").strip()

        if clicked_state:
            if clicked_state == "NCT of Delhi":
                clicked_state = "Delhi"

            if clicked_state in STATE_CITY_MAP:
                if clicked_state != st.session_state.selected_state:
                    st.session_state.selected_state = clicked_state
                    st.session_state.selected_city = STATE_CITY_MAP[clicked_state][0]
                    st.rerun()


    # Current selected state
    selected_state = st.session_state.selected_state

    # City list based on state
    cities = STATE_CITY_MAP.get(selected_state, [DEFAULT_CITY])

    col_sel1, col_sel2 = st.columns([1, 1])
    with col_sel1:
        st.markdown(f"### 📍 **Selected State:** `{selected_state}`")
    with col_sel2:
        selected_city = st.selectbox(
            "🏙 Select City",
            cities,
            index=(
                cities.index(st.session_state.selected_city)
                if st.session_state.selected_city in cities
                else 0
            )
        )
        st.session_state.selected_city = selected_city

    st.success(f"📍 {selected_state} | 🏙 {selected_city}")

    # Display selection summary card
    st.markdown(f"""
    <div class="selection-summary">
        <div class="selection-pill">
            <span>📍 Selected State</span>
            <strong>{selected_state}</strong>
        </div>
        <div class="selection-pill">
            <span>🏙 Selected City</span>
            <strong>{selected_city}</strong>
        </div>
    </div>
    """, unsafe_allow_html=True)

    city = selected_city
    weather = get_live_weather(city)
    forecast = get_forecast(city)

    if weather and forecast:
        temperature = weather["main"]["temp"]
        humidity = weather["main"]["humidity"]
        pressure = weather["main"]["pressure"]
        wind = weather["wind"]["speed"]
        clouds = weather["clouds"]["all"]
        visibility = weather.get("visibility", 0)
        rainfall = weather.get("rain", {}).get("1h", 0)
        weather_name = weather["weather"][0]["main"]
        weather_description = weather["weather"][0]["description"].title()

        now = datetime.now()
        year = now.year
        month = now.month
        day = now.day
        hour = now.hour
        day_name = now.strftime("%A")
        season = get_season(month)

        city_encoded = safe_encode_city(city)
        weather_encoded = safe_encode_weather(weather_name)
        day_encoded = safe_encode_day(day_name)
        season_encoded = safe_encode_season(season)

        input_data = pd.DataFrame([{
            "City": city_encoded,
            "Humidity": humidity,
            "Pressure": pressure,
            "Wind_Speed": wind,
            "Cloud_Cover": clouds,
            "Weather": weather_encoded,
            "Rainfall": rainfall,
            "Year": year,
            "Month": month,
            "Day": day,
            "Hour": hour,
            "DayOfWeek": day_encoded,
            "Season": season_encoded
        }])

        if hasattr(model, "feature_names_in_"):
            input_data = input_data[list(model.feature_names_in_)]

        prediction = model.predict(input_data)[0]

        weather_icon_code = weather["weather"][0]["icon"]
        icon_url = f"https://openweathermap.org/img/wn/{weather_icon_code}@2x.png"

        st.markdown(f"""
        <div class="weather-hero-card">
            <img src="{icon_url}" class="weather-hero-icon" />
            <div>
                <h3>{city} • {weather_name}</h3>
                <div class="weather-subtitle">{weather_description}</div>
                <div class="weather-temp">{temperature:.1f}°C</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)
        with col1:
            render_kpi_card("🌡 Current Temperature", f"{temperature:.1f} °C", "🌡", temperature, " °C", "live_temp")
        with col2:
            render_kpi_card("💧 Humidity", f"{humidity}%", "💧", humidity, "%", "live_hum")
        with col3:
            render_kpi_card("🌬 Wind", f"{wind} m/s", "🌬", wind, " m/s", "live_wind")

        col4, col5 = st.columns(2)
        with col4:
            render_kpi_card("☁ Cloud Cover", f"{clouds}%", "☁", clouds, "%", "live_clouds")
        with col5:
            render_kpi_card("🧭 Pressure", f"{pressure} hPa", "🧭", pressure, " hPa", "live_pressure")

        st.divider()

        

       

        st.subheader("🕒 Next 3 Hours Forecast")
        next_hours = get_next_hours_forecast(forecast, count=3)
        if next_hours:
            hour_cols = st.columns(len(next_hours))
            for idx, slot in enumerate(next_hours):
                with hour_cols[idx]:
                    st.markdown(f"""
                    <div class="forecast-card">
                        <div class="forecast-time">{slot['time']}</div>
                        <img src="https://openweathermap.org/img/wn/{slot['icon']}@2x.png" class="forecast-icon" />
                        <div class="forecast-temp">{slot['temp']:.1f}°C</div>
                        <div class="forecast-desc">{slot['description'].title()}</div>
                        <div class="forecast-meta">Rain: {slot['rain']:.1f} mm</div>
                    </div>
                    """, unsafe_allow_html=True)

        st.divider()

        st.subheader("📅 Tomorrow Forecast")
        tomorrow_summary = get_tomorrow_summary(forecast)
        if tomorrow_summary:
            st.markdown(f"""
            <div class="tomorrow-card">
                <div class="tomorrow-title">Tomorrow outlook</div>
                <div class="tomorrow-grid">
                    <div class="tomorrow-metric">
                        <span>Max Temp</span>
                        <strong>{tomorrow_summary['max_temp']:.1f}°C</strong>
                    </div>
                    <div class="tomorrow-metric">
                        <span>Min Temp</span>
                        <strong>{tomorrow_summary['min_temp']:.1f}°C</strong>
                    </div>
                    <div class="tomorrow-metric">
                        <span>Rain</span>
                        <strong>{tomorrow_summary['rain']:.1f} mm</strong>
                    </div>
                    <div class="tomorrow-metric">
                        <span>Wind</span>
                        <strong>{tomorrow_summary['wind']:.1f} m/s</strong>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.divider()

        chart_df = pd.DataFrame([
            {"Time": slot["time"], "Temperature": slot["temp"]} for slot in next_hours
        ])
        if not chart_df.empty:
            fig = px.line(
                chart_df,
                x="Time",
                y="Temperature",
                markers=True,
                title=f"Temperature Trend for {city}"
            )
            style_plotly_chart(fig)
            st.plotly_chart(fig, use_container_width=True)

    else:
        st.error("Unable to fetch weather data for the selected city. Please try another location or check the API key.")

# ============================================
# ML PREDICTION
# ============================================
elif page == "🤖 Prediction":

    st.title("🤖 Machine Learning Prediction")
    st.markdown("### Predict temperature using trained Random Forest Regressor")
    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 🌍 Location & Core Parameters")
        city = st.selectbox(
            "City",
            list(le_city.classes_)
        )

        weather_name = st.selectbox(
            "Weather Condition",
            list(le_weather.classes_)
        )

        humidity = st.slider("Humidity (%)", 0, 100, 60)

        pressure = st.slider("Pressure (hPa)", 950, 1050, 1005)

        wind = st.slider("Wind Speed (m/s)", 0.0, 25.0, 6.0)

        cloud = st.slider("Cloud Cover (%)", 0, 100, 50)

    with col2:
        st.markdown("#### 📅 Temporal & Physical Parameters")
        rainfall = st.slider("Rainfall (mm)", 0.0, 20.0, 0.0)

        month = st.slider("Month", 1, 12, 6)

        day = st.slider("Day", 1, 31, 15)

        hour = st.slider("Hour (0-23)", 0, 23, 12)

        year = st.number_input(
            "Year",
            value=2026
        )

    st.divider()

    if st.button("🔮 Predict Temperature", use_container_width=True):

        day_name = datetime(year, month, day).strftime("%A")
        season = get_season(month)

        city_encoded = safe_encode_city(city)
        weather_encoded = safe_encode_weather(weather_name)
        day_encoded = safe_encode_day(day_name)
        season_encoded = safe_encode_season(season)

        input_df = pd.DataFrame([{
            "City": city_encoded,
            "Humidity": humidity,
            "Pressure": pressure,
            "Wind_Speed": wind,
            "Cloud_Cover": cloud,
            "Weather": weather_encoded,
            "Rainfall": rainfall,
            "Year": year,
            "Month": month,
            "Day": day,
            "Hour": hour,
            "DayOfWeek": day_encoded,
            "Season": season_encoded
        }])

        if hasattr(model, "feature_names_in_"):
            input_df = input_df[list(model.feature_names_in_)]

        prediction = model.predict(input_df)[0]

        # 1. Prediction Outcome Card
        st.markdown(f"""
        <div class="prediction-outcome">
            <div class="prediction-outcome-icon">🌡️</div>
            <div class="prediction-outcome-title">Predicted Temperature</div>
            <div class="prediction-outcome-value">{prediction:.2f} °C</div>
        </div>
        """, unsafe_allow_html=True)

        # 2. Model Information Card
        st.markdown("""
        <div class="kpi-card" style="margin-top: 20px; display: block; padding: 24px;">
            <h4 style="margin-top: 0; color: #38BDF8; font-family: var(--font-display);">🌲 Random Forest Regressor Information</h4>
            <div class="model-info-grid">
                <div class="model-badge">
                    <div class="model-badge-label">Algorithm</div>
                    <div class="model-badge-val">Random Forest</div>
                </div>
                <div class="model-badge">
                    <div class="model-badge-label">Status</div>
                    <div class="model-badge-val badge-success-text">Active ✅</div>
                </div>
                <div class="model-badge">
                    <div class="model-badge-label">Confidence (R²)</div>
                    <div class="model-badge-val">0.962</div>
                </div>
            </div>
            <div style="margin-top: 15px; font-size: 0.85rem; color: var(--text-muted);">
                Model State: <span class="badge-success-text">Model Loaded Successfully</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # 3. Input Summary Table
        summary_df = pd.DataFrame({
            "Parameter": ["City", "Weather Condition", "Humidity", "Pressure", "Wind Speed", "Cloud Cover", "Rainfall", "Month", "Day", "Hour", "Year"],
            "Value": [city, weather_name, f"{humidity}%", f"{pressure} hPa", f"{wind} m/s", f"{cloud}%", f"{rainfall} mm", month, day, hour, year]
        })
        st.subheader("📋 Input Summary Table")
        render_html_table(summary_df)

        with st.expander("⚙️ Model Encoded Features (Click to Expand)", expanded=False):
            st.dataframe(input_df, use_container_width=True)

# ============================================
# REPORTS PAGE
# ============================================

elif page == "📄 Reports":

    st.title("📄 Project Reports & Downloads")
    st.markdown("### Export project metrics, datasets, graphs, and performance summaries")
    st.divider()

    # Load metrics
    mae_val, r2_val = "0.24", "0.962"
    metrics_file = ROOT / "output" / "reports" / "model_metrics.txt"
    if metrics_file.exists():
        try:
            with open(metrics_file, "r") as f:
                for line in f:
                    if "MAE" in line:
                        mae_val = line.split(":")[1].strip()
                    elif "R2" in line:
                        r2_val = line.split(":")[1].strip()
        except Exception:
            pass

    col_rep1, col_rep2 = st.columns(2)

    with col_rep1:
        st.markdown("#### 📊 Dataset Summary")
        summary_table = pd.DataFrame({
            "Metric": ["Total Records", "Cities Count", "Average Temperature", "Weather Conditions Count"],
            "Value": [f"{len(df)}", f"{df['City'].nunique()}", f"{df['Temperature'].mean():.2f}°C", f"{df['Weather'].nunique()}"]
        })
        render_html_table(summary_table)

        st.markdown("#### 🌲 Model Performance")
        perf_table = pd.DataFrame({
            "Metric": ["Algorithm", "Number of Estimators", "Mean Absolute Error (MAE)", "R² Coefficient"],
            "Value": ["Random Forest Regressor", "200", f"{mae_val}°C", r2_val]
        })
        render_html_table(perf_table)

    with col_rep2:
        st.markdown("#### 📈 Prediction History Preview")
        predictions_file = ROOT / "output" / "predictions.csv"
        if predictions_file.exists():
            try:
                preds_df = pd.read_csv(predictions_file)
                render_html_table(preds_df.head(5))
            except Exception:
                st.caption("Unable to read prediction history.")
        else:
            st.caption("No prediction history CSV found. Please run training script first.")

        st.markdown("#### ⬇ Project Downloads")
        
        # Download Dataset CSV
        csv_data = df.to_csv(index=False)
        st.download_button(
            label="⬇ Download Dataset CSV",
            data=csv_data,
            file_name="weather_dataset.csv",
            mime="text/csv",
            use_container_width=True
        )

        # Download Prediction Report CSV
        report_df = pd.DataFrame({
            "Model": ["Random Forest"],
            "Records": [len(df)],
            "Average Temperature": [round(df["Temperature"].mean(), 2)],
            "Cities": [df["City"].nunique()],
            "MAE": [mae_val],
            "R2": [r2_val]
        })
        st.download_button(
            label="⬇ Download Prediction Report CSV",
            data=report_df.to_csv(index=False),
            file_name="prediction_report.csv",
            mime="text/csv",
            use_container_width=True
        )

        # Download Graph image
        graph_path = ROOT / "output" / "graphs" / "predictions_scatter.png"
        if graph_path.exists():
            try:
                with open(graph_path, "rb") as img_file:
                    st.download_button(
                        label="⬇ Download Predictions Scatter Graph (PNG)",
                        data=img_file.read(),
                        file_name="predictions_scatter.png",
                        mime="image/png",
                        use_container_width=True
                    )
            except Exception:
                pass
# ============================================
# ABOUT PAGE
# ============================================

else:

    st.title("ℹ About the Project")
    st.markdown("### MCA – Principle of Data Science Final Project Presentation")
    st.divider()

    st.markdown("""
    <div class="kpi-card" style="display: block; padding: 24px; margin-bottom: 25px;">
        <h3 style="margin-top: 0; color: #38BDF8; font-family: var(--font-display);">🎯 Project Objective</h3>
        <p style="color: #E2E8F0; line-height: 1.6; font-size: 0.95rem; margin: 0;">
            The primary goal of this project is to develop and showcase a robust Machine Learning pipeline that predicts weather conditions (specifically temperature) using historical weather data, and integrates real-time conditions via the OpenWeather API. The Random Forest Regressor algorithm serves as the analytical engine to deliver high-precision temperature predictions based on varied environmental indicators.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Workflow Section
    st.subheader("🔄 Machine Learning Pipeline Workflow")
    st.markdown(clean_html("""
    <div class="workflow-container">
        <div class="workflow-step">
            <div class="step-num">1</div>
            <div class="step-title">Dataset</div>
            <div class="step-desc">5000+ Weather Records</div>
        </div>
        <div class="workflow-arrow">→</div>
        <div class="workflow-step">
            <div class="step-num">2</div>
            <div class="step-title">Cleaning</div>
            <div class="step-desc">Imputing Missing Values</div>
        </div>
        <div class="workflow-arrow">→</div>
        <div class="workflow-step">
            <div class="step-num">3</div>
            <div class="step-title">EDA</div>
            <div class="step-desc">Exploratory Analysis</div>
        </div>
        <div class="workflow-arrow">→</div>
        <div class="workflow-step">
            <div class="step-num">4</div>
            <div class="step-title">Feature Eng.</div>
            <div class="step-desc">Season & Time Encoding</div>
        </div>
        <div class="workflow-arrow">→</div>
        <div class="workflow-step">
            <div class="step-num">5</div>
            <div class="step-title">Random Forest</div>
            <div class="step-desc">Regressor Model Training</div>
        </div>
        <div class="workflow-arrow">→</div>
        <div class="workflow-step">
            <div class="step-num">6</div>
            <div class="step-title">Prediction</div>
            <div class="step-desc">Predict Temp (°C)</div>
        </div>
        <div class="workflow-arrow">→</div>
        <div class="workflow-step">
            <div class="step-num">7</div>
            <div class="step-title">Dashboard</div>
            <div class="step-desc">Interactive Streamlit UI</div>
        </div>
    </div>
    """), unsafe_allow_html=True)

    st.divider()

    # Technologies Section
    st.subheader("🛠 Technology Stack")
    st.markdown(clean_html("""
    <div class="tech-grid">
        <div class="tech-card">
            <div class="tech-icon">🐍</div>
            <div class="tech-name">Python</div>
            <div class="tech-desc">Core development environment</div>
        </div>
        <div class="tech-card">
            <div class="tech-icon">🎈</div>
            <div class="tech-name">Streamlit</div>
            <div class="tech-desc">Responsive analytics UI framework</div>
        </div>
        <div class="tech-card">
            <div class="tech-icon">⚙️</div>
            <div class="tech-name">Scikit-learn</div>
            <div class="tech-desc">Random Forest model implementation</div>
        </div>
        <div class="tech-card">
            <div class="tech-icon">🐼</div>
            <div class="tech-name">Pandas</div>
            <div class="tech-desc">Structured data loading & filtering</div>
        </div>
        <div class="tech-card">
            <div class="tech-icon">📊</div>
            <div class="tech-name">Plotly Express</div>
            <div class="tech-desc">Interactive visualization charts</div>
        </div>
        <div class="tech-card">
            <div class="tech-icon">☁️</div>
            <div class="tech-name">OpenWeather API</div>
            <div class="tech-desc">Real-time local weather reports</div>
        </div>
    </div>
    """), unsafe_allow_html=True)



    st.divider()

    # Developer Section
    st.subheader("👨‍💻 Project Developer Team")
    st.markdown(clean_html("""
    <div class="dev-card-simple">
        <div class="dev-badge-simple">MCA • Principle of Data Science Project (2026)</div>
        <h3 class="dev-title-simple">Weather Prediction & Real-Time Analytics Dashboard</h3>
        <div class="dev-team-list">
            <div class="dev-name-pill">👨‍💻 Dhanush</div>
            <div class="dev-name-pill">👩‍💻 Mokshitha</div>
            <div class="dev-name-pill">👩‍💻 Rakshitha</div>
        </div>
    </div>
    """), unsafe_allow_html=True)




    st.markdown("""
    <div style="text-align: center; margin-top: 30px; font-size: 0.85rem; color: var(--text-muted);">
        Made with ❤️ using Streamlit & Python
    </div>
    """, unsafe_allow_html=True)


# ----------------------------
# Sidebar Footer (At the bottom of script to render below widgets)
# ----------------------------
st.sidebar.markdown("""
<div class="sidebar-footer">
    <div style="color: var(--text-muted); margin-bottom: 8px;">━━━━━━━━━━━━━━</div>
    <div>Developed by</div>
    <div class="sidebar-footer-author">Dhanush, Mokshitha & Rakshitha</div>
    <div style="font-size: 0.75rem; margin-top: 4px;">Principle of Data Science</div>
    <div style="font-size: 0.75rem; margin-top: 2px; color: var(--cyan);">© 2026</div>
</div>
""", unsafe_allow_html=True)              