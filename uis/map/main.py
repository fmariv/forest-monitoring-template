import streamlit as st
import pandas as pd
import requests
import pydeck as pdk
import os

from spai.project import ProjectConfig


project = ProjectConfig()

base_url = 'http://localhost'   # TODO control this with env vars
analytics_url = f'{base_url}:{project.api_port("analytics")}'
xyz_url = f'{base_url}:{project.api_port("xyz")}'


st.set_page_config(page_title="SPAI Demo", page_icon="🌍")


@st.cache_data(ttl=10)
def get_data():  # in cloud fails because localhost is inside docker, need public url
    api_url = analytics_url
    analytics = requests.get(api_url).json()
    df = pd.DataFrame(analytics)
    return df


df = get_data()

# AWS Open Data Terrain Tiles
TERRAIN_IMAGE = (
    "https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{z}/{x}/{y}.png"
)

# Define how to parse elevation tiles
ELEVATION_DECODER = {"rScaler": 256, "gScaler": 1, "bScaler": 1 / 256, "offset": -32768}

st.sidebar.markdown("### Dates")

selected_layers = [
    pdk.Layer(
        "TerrainLayer",
        texture=f"{xyz_url}/NDVI_{date}.tif/{{z}}/{{x}}/{{y}}.png",
        elevation_decoder=ELEVATION_DECODER,
        elevation_data=TERRAIN_IMAGE,
    )
    for date in df.index
    if st.sidebar.checkbox(date, True)
]

if selected_layers:
    st.pydeck_chart(
        pdk.Deck(
            map_style="mapbox://styles/mapbox/light-v9",
            initial_view_state={
                "latitude": 41.4,   # TODO center on AOI
                "longitude": 2.17,
                "zoom": 9,
                "pitch": 60,
            },
            layers=selected_layers,
        )
    )
else:
    st.error("Please choose at least one layer above.")

st.title("Vegetation Analytics")

st.line_chart(df)
if st.checkbox("Show data"):
    st.write(df)
