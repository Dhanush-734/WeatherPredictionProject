from pathlib import Path
import geopandas as gpd
import plotly.graph_objects as go

# ------------------------------------------------------------------
# File Path
# ------------------------------------------------------------------
ROOT = Path(__file__).resolve().parents[1]
GEOJSON_PATH = ROOT / "assets" / "India_State.geojson"

# ------------------------------------------------------------------
# State -> Cities
# ------------------------------------------------------------------
STATE_CITY_MAP = {
    "Karnataka": ["Bangalore", "Mangalore", "Mysore"],
    "Maharashtra": ["Mumbai", "Pune"],
    "Tamil Nadu": ["Chennai"],
    "Kerala": ["Kochi"],
    "Delhi": ["Delhi"],
    "Gujarat": ["Ahmedabad"],
    "Rajasthan": ["Jaipur"],
    "West Bengal": ["Kolkata"],
    "Madhya Pradesh": ["Bhopal"],
    "Telangana": ["Hyderabad"],
    "Uttar Pradesh": ["Lucknow"],
    "Goa": ["Goa"],
}

# ------------------------------------------------------------------
# Load GeoJSON
# ------------------------------------------------------------------
def load_state_geojson():

    print("=" * 50)
    print("Loading GeoJSON...")
    print("Path:", GEOJSON_PATH)
    print("Exists:", GEOJSON_PATH.exists())
    print("=" * 50)

    if not GEOJSON_PATH.exists():
        raise FileNotFoundError(f"GeoJSON not found:\n{GEOJSON_PATH}")

    gdf = gpd.read_file(GEOJSON_PATH)

    print("Columns:", gdf.columns.tolist())

    return gdf


# ------------------------------------------------------------------
# Build India Map
# ------------------------------------------------------------------
def build_india_map(selected_state=None):

    gdf = load_state_geojson()

    # Your uploaded GeoJSON contains NAME_1
    if "NAME_1" not in gdf.columns:
        raise Exception(
            f"'NAME_1' column not found.\nAvailable columns:\n{gdf.columns.tolist()}"
        )

    gdf["state_name"] = gdf["NAME_1"].astype(str)

    # Keep only supported states
    gdf = gdf[gdf["state_name"].isin(STATE_CITY_MAP.keys())]

    gdf["selected"] = gdf["state_name"] == (selected_state or "")

    fig = go.Figure()

    fig.add_trace(
        go.Choroplethmapbox(
            geojson=gdf.__geo_interface__,
            locations=gdf["state_name"],
            z=gdf["selected"].astype(int),

            # IMPORTANT
            featureidkey="properties.NAME_1",

            colorscale=[
                [0, "#334155"],
                [1, "#38BDF8"]
            ],

            marker_line_width=1,
            marker_line_color="white",

            showscale=False,

            hovertemplate="<b>%{location}</b><extra></extra>",
        )
    )

    fig.update_layout(

        mapbox_style="carto-positron",

        mapbox_zoom=3.7,

        mapbox_center={
            "lat": 22.5,
            "lon": 79
        },

        margin=dict(
            l=0,
            r=0,
            t=0,
            b=0
        ),

        height=450,

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="rgba(0,0,0,0)",
    )

    return fig