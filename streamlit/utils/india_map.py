from pathlib import Path
import geopandas as gpd
import plotly.graph_objects as go
from streamlit_plotly_events import plotly_events


# Current project path
ROOT = Path(__file__).resolve().parents[1]

# Correct GeoJSON location
GEOJSON_PATH = ROOT / "assets" / "India_State.geojson"


STATE_CITY_MAP = {
    "Karnataka": ["Bangalore", "Mangalore", "Mysore"],
    "Maharashtra": ["Mumbai", "Pune", "Nagpur"],
    "Tamil Nadu": ["Chennai", "Coimbatore", "Madurai"],
    "Kerala": ["Kochi", "Thiruvananthapuram", "Kozhikode"],
    "Delhi": ["Delhi", "New Delhi", "Dwarka"],
    "NCT of Delhi": ["Delhi", "New Delhi", "Dwarka"],
    "Gujarat": ["Ahmedabad", "Surat", "Vadodara"],
    "Rajasthan": ["Jaipur", "Udaipur", "Jodhpur"],
    "West Bengal": ["Kolkata", "Siliguri", "Durgapur"],
    "Madhya Pradesh": ["Bhopal", "Indore", "Gwalior"],
    "Telangana": ["Hyderabad", "Warangal", "Nizamabad"],
    "Uttar Pradesh": ["Lucknow", "Varanasi", "Agra"],
    "Goa": ["Goa", "Panaji", "Margao"],
    "Andhra Pradesh": ["Visakhapatnam", "Vijayawada", "Tirupati"],
    "Andaman and Nicobar": ["Port Blair", "Havelock"],
    "Arunachal Pradesh": ["Itanagar", "Tawang", "Pasighat"],
    "Assam": ["Guwahati", "Dibrugarh", "Silchar"],
    "Bihar": ["Patna", "Gaya", "Muzaffarpur"],
    "Chandigarh": ["Chandigarh", "Delhi"],
    "Chhattisgarh": ["Raipur", "Bhilai", "Bilaspur"],
    "Dadra and Nagar Haveli": ["Silvassa", "Daman", "Mumbai"],
    "Daman and Diu": ["Daman", "Diu", "Ahmedabad"],
    "Haryana": ["Gurugram", "Faridabad", "Ambala"],
    "Himachal Pradesh": ["Shimla", "Manali", "Dharamshala"],
    "Jammu and Kashmir": ["Srinagar", "Jammu", "Anantnag"],
    "Jharkhand": ["Ranchi", "Jamshedpur", "Dhanbad"],
    "Lakshadweep": ["Kavaratti", "Agatti"],
    "Manipur": ["Imphal", "Churachandpur", "Thoubal"],
    "Meghalaya": ["Shillong", "Tura", "Jowai"],
    "Mizoram": ["Aizawl", "Lunglei", "Champhai"],
    "Nagaland": ["Kohima", "Dimapur", "Mokokchung"],
    "Odisha": ["Bhubaneswar", "Cuttack", "Puri"],
    "Puducherry": ["Puducherry", "Karaikal"],
    "Punjab": ["Amritsar", "Ludhiana", "Jalandhar"],
    "Sikkim": ["Gangtok", "Namchi", "Pelling"],
    "Tripura": ["Agartala", "Udaipur", "Dharmanagar"],
    "Uttarakhand": ["Dehradun", "Haridwar", "Nainital"],
}




def load_state_geojson():

    print("GeoJSON PATH:", GEOJSON_PATH)
    print("FOUND:", GEOJSON_PATH.exists())

    if not GEOJSON_PATH.exists():
        return None

    gdf = gpd.read_file(GEOJSON_PATH)

    print("ROWS:", len(gdf))
    print("COLUMNS:", gdf.columns.tolist())

    if len(gdf) > 0:
        print(
            "FIRST ROW:",
            gdf.iloc[0]
        )

    return gdf

from typing import Optional
def build_india_map(selected_state: Optional[str] = None):
    gdf = load_state_geojson()
    if gdf is None:
        return None

    gdf = gdf.copy()
    state_name_column = None
    for candidate in ["state_name", "NAME_1", "name", "STATE", "State"]:
        if candidate in gdf.columns:
            state_name_column = candidate
            break
    if state_name_column is None:
        gdf["state_name"] = [
            feature.get("properties", {}).get("state_name", "")
            for feature in gdf.__geo_interface__.get("features", [])
        ]
    else:
        gdf["state_name"] = gdf[state_name_column].astype(str)

    gdf["is_selected"] = gdf["state_name"].eq(selected_state or "")
    # Keep all Indian states
    gdf = gdf.copy()

    fig = go.Figure()
    fig.add_trace(
        go.Choroplethmapbox(
            geojson=gdf.__geo_interface__,
            locations=gdf["state_name"],
            z=gdf["is_selected"].astype(int),
            featureidkey="properties.NAME_1",
            colorscale=[[0, "#1E293B"], [1, "#38BDF8"]],
            showscale=False,
            marker_opacity=0.85,
            hovertemplate="<b>%{location}</b><extra></extra>",
            marker_line_width=1,
            marker_line_color="white",
        )
    )

    fig.update_layout(
        mapbox_style="carto-positron",
        mapbox_zoom=3.4,
        mapbox_center={"lat": 22.5, "lon": 78.9},
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=420,
    )

    return fig
