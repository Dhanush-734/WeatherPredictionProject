import json
import folium
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GEOJSON_PATH = ROOT / "assets" / "India_State.geojson"
GEOJSON_SIMPLIFIED_PATH = ROOT / "assets" / "India_State_simplified.geojson"


from typing import Optional

def create_india_map(selected_state: Optional[str] = None):
    geojson_path = (
        GEOJSON_SIMPLIFIED_PATH
        if GEOJSON_SIMPLIFIED_PATH.exists()
        else GEOJSON_PATH
    )
    with open(geojson_path, "r", encoding="utf-8") as f:
        geojson_data = json.load(f)

    india = folium.Map(
        location=[22.5, 78.9],
        zoom_start=4.5,
        tiles="CartoDB positron",
        width="100%",
        height="100%",
        zoom_control=True,
        scrollWheelZoom=False,
    )

    # Ensure map iframe body and container fill 100% and remove any black bottom gap
    macro = folium.Element("""
    <style>
        html, body {
            margin: 0 !important;
            padding: 0 !important;
            height: 100% !important;
            width: 100% !important;
            background-color: #d5dadc !important;
            overflow: hidden !important;
        }
        .folium-map {
            width: 100% !important;
            height: 100% !important;
        }
        .leaflet-container {
            background: #d5dadc !important;
        }
    </style>
    """)
    india.get_root().html.add_child(macro)

    def style_function(feature):
        props = feature.get("properties", {})
        state_name = props.get("NAME_1", "")

        is_selected = False
        if selected_state:
            if state_name.lower() == selected_state.lower() or (
                selected_state == "Delhi" and state_name == "NCT of Delhi"
            ):
                is_selected = True

        if is_selected:
            return {
                "fillColor": "#0284c7",
                "color": "#0369a1",
                "weight": 3,
                "fillOpacity": 0.85,
            }
        else:
            return {
                "fillColor": "#2563eb",
                "color": "#ffffff",
                "weight": 1.2,
                "fillOpacity": 0.45,
            }

    def highlight_function(feature):
        return {
            "fillColor": "#38bdf8",
            "color": "#ffffff",
            "weight": 2.5,
            "fillOpacity": 0.9,
        }

    folium.GeoJson(
        geojson_data,
        name="India States",
        style_function=style_function,
        highlight_function=highlight_function,
        tooltip=folium.GeoJsonTooltip(
            fields=["NAME_1"],
            aliases=["State: "],
            style="font-family: 'Inter', sans-serif; font-size: 13px; font-weight: 600; padding: 4px 8px; color: #0f172a; background-color: #ffffff; border-radius: 4px; border: 1px solid #cbd5e1;",
        ),
    ).add_to(india)

    return india

