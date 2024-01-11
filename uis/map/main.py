"""
Streamlit app with Folium to display vegetation analytics
"""
import os

import folium
from streamlit_folium import folium_static
import geopandas as gpd
import pandas as pd
import requests
import streamlit as st
from spai.models import ProjectConfig


project = ProjectConfig()

BASE_URL = "http://localhost"
ANALYTICS_URL = f'{BASE_URL}:{project.api_port("analytics")}'
XYZ_URL = f'{BASE_URL}:{project.api_port("xyz")}'

VARIABLES_STRETCH = {
    "vegetation": "0,1",
    "quality": "0,3",
}


@st.cache_data(ttl=10)
def get_data():
    """
    Get vegetation analytics data

    Returns
    -------
    df : pandas.DataFrame
        Dataframe with vegetation analytics data
    """
    api_url = ANALYTICS_URL
    analytics = requests.get(api_url, timeout=10).json()
    analytics_df = pd.DataFrame(analytics)
    analytics_df.sort_index(inplace=True)
    return analytics_df


def get_aoi_centroid():
    """
    Get AoI centroid

    Returns
    -------
    centroid : tuple
        AOI centroid
    """
    aoi = project.aoi
    gdf = gpd.GeoDataFrame.from_features(aoi)
    centroid = gdf.geometry.centroid[0].y, gdf.geometry.centroid[0].x

    return centroid


def choose_variables():
    """
    Choose date and variable from the analytics data

    Returns
    -------
    date : str
        Date from the analytics data
    variable : str
        Variable from the analytics data
    """
    with st.sidebar:
        st.sidebar.markdown("### Select date and indicator")
        date = st.selectbox("Date", df.index)
        variable = st.selectbox("Indicator", ["Vegetation", "Quality"])
        variable = variable.lower()
    return date, variable


st.set_page_config(page_title="Forest monitoring Pulse", page_icon="🌳")

df = get_data()  # Get data from the API
centroid = get_aoi_centroid()  # Get centroid from the AOI

date, variable = choose_variables()  # Choose date and variable from the data

url = f"{XYZ_URL}/{variable}_masked_{date}.tif/{{z}}/{{x}}/{{y}}.png?palette=RdYlGn&stretch={VARIABLES_STRETCH[variable]}"

# Create map with Folium
m = folium.Map(
    location=centroid,
    zoom_start=12,
    tiles="CartoDB Positron",
)
# Add the analytic layer to the map
raster = folium.raster_layers.TileLayer(
    tiles=url,
    attr="Forest monitoring Pulse",
    name="Vegetation",
    overlay=True,
    control=True,
    show=True,
)
raster.add_to(m)
folium_static(m)

# Plot vegetation analytics data
st.title("Vegetation Analytics")

colors = ["#e41a1c", "#BFEAA2", "#E4EA20", "#245900"]

df_chart = df.drop(columns=["Total"])  # Remove Total column to not plot it
st.line_chart(df_chart, color=colors)
if st.checkbox("Show data"):
    st.write(df)
