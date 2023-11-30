"""
Streamlit app to display vegetation analytics
"""
import os

import geopandas as gpd
import pandas as pd
import pydeck as pdk
import requests
import streamlit as st
from spai.project import ProjectConfig

project = ProjectConfig()

base_url = "http://localhost"  # TODO control this with env vars
analytics_url = f'{base_url}:{project.api_port("analytics")}'
xyz_url = f'{base_url}:{project.api_port("xyz")}'


@st.cache_data(ttl=10)
def get_data():
    """
    Get vegetation analytics data

    Returns
    -------
    df : pandas.DataFrame
        Dataframe with vegetation analytics data
    """
    api_url = analytics_url
    analytics = requests.get(api_url, timeout=10).json()
    analytics_df = pd.DataFrame(analytics)
    return analytics_df


def get_aoi_centroid():
    """
    Get AOI centroid

    Returns
    -------
    centroid : tuple
        AOI centroid
    """
    aoi = project.aoi
    gdf = gpd.GeoDataFrame.from_features(aoi)
    centroid = gdf.geometry.centroid[0].x, gdf.geometry.centroid[0].y

    return centroid


st.set_page_config(page_title="Forest monitoring Pulse", page_icon="🌳")

df = get_data()
centroid = get_aoi_centroid()

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
        texture=f"{xyz_url}/ndvi_{date}.tif/{{z}}/{{x}}/{{y}}.png?palette=RdYlGn",
        elevation_decoder=ELEVATION_DECODER,
        elevation_data=TERRAIN_IMAGE,
    )
    for date in df.index
    if st.sidebar.checkbox(date, True)
]

view_state = pdk.ViewState(
    latitude=centroid[1], longitude=centroid[0], zoom=9, pitch=60
)

if selected_layers:
    st.pydeck_chart(
        pdk.Deck(
            map_style="mapbox://styles/mapbox/light-v9",
            initial_view_state=view_state,
            layers=selected_layers,
        )
    )
else:
    st.error("Please choose at least one layer above.")

st.title("Vegetation Analytics")

st.line_chart(df)
if st.checkbox("Show data"):
    st.write(df)
