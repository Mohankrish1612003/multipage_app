import streamlit as st
import pandas as pd
import pydeck as pdk
from urllib.error import URLError

st.set_page_config(page_title="Geospatial Demo", page_icon="🌍")

st.markdown("# Geospatial Mapping")
st.sidebar.header("Geospatial Demo")
st.write(
    """Here is an example demonstrating how to leverage 
[`st.pydeck_chart`](https://docs.streamlit.io/develop/api-reference/charts/st.pydeck_chart) 
for rendering 3D maps and geospatial visualizations."""
)

@st.cache_data
def fetch_dataset(file_name):
    """Retrieves JSON map data from the Streamlit demo repository."""
    base_url = "http://raw.githubusercontent.com/streamlit/example-data/master/hello/v1/"
    return pd.read_json(f"{base_url}{file_name}")

try:
    # Define the 3D map layers
    AVAILABLE_LAYERS = {
        "Bike Rentals": pdk.Layer(
            "HexagonLayer",
            data=fetch_dataset("bike_rental_stats.json"),
            get_position=["lon", "lat"],
            radius=200,
            elevation_scale=4,
            elevation_range=[0, 1000],
            extruded=True,
        ),
        "Bart Stop Exits": pdk.Layer(
            "ScatterplotLayer",
            data=fetch_dataset("bart_stop_stats.json"),
            get_position=["lon", "lat"],
            get_color=[200, 30, 0, 160],
            get_radius="[exits]",
            radius_scale=0.05,
        ),
        "Bart Stop Names": pdk.Layer(
            "TextLayer",
            data=fetch_dataset("bart_stop_stats.json"),
            get_position=["lon", "lat"],
            get_text="name",
            get_color=[0, 0, 0, 200],
            get_size=15,
            get_alignment_baseline="'bottom'",
        ),
        "Outbound Flow": pdk.Layer(
            "ArcLayer",
            data=fetch_dataset("bart_path_stats.json"),
            get_source_position=["lon", "lat"],
            get_target_position=["lon2", "lat2"],
            get_source_color=[200, 30, 0, 160],
            get_target_color=[200, 30, 0, 160],
            auto_highlight=True,
            width_scale=0.0001,
            get_width="outbound",
            width_min_pixels=3,
            width_max_pixels=30,
        ),
    }
    
    # Sidebar toggles for each layer
    st.sidebar.markdown("### Toggle Map Layers")
    active_layers = [
        map_layer
        for name, map_layer in AVAILABLE_LAYERS.items()
        if st.sidebar.checkbox(name, value=True)
    ]
    
    # Render the pydeck chart if layers are selected
    if active_layers:
        st.pydeck_chart(
            pdk.Deck(
                map_style="mapbox://styles/mapbox/light-v9",
                initial_view_state={
                    "latitude": 37.76,
                    "longitude": -122.4,
                    "zoom": 11,
                    "pitch": 50,
                },
                layers=active_layers,
            )
        )
    else:
        st.error("Please enable at least one map layer to view the chart.")
        
except URLError as error:
    st.error(f"**Internet access is required to run this demo.**\n\nConnection error: {error.reason}")