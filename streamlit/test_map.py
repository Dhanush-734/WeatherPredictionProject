import streamlit as st
from utils.india_folium_map import create_india_map
from streamlit_folium import st_folium

st.title("TEST MAP")

m = create_india_map()

st_folium(
    m,
    width=1200,
    height=700
)