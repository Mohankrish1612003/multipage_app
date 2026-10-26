import streamlit as st
import pandas as pd
import altair as alt
from urllib.error import URLError

st.set_page_config(page_title="DataFrames in Action", page_icon="📊")

st.markdown("# DataFrame Visualizer")
st.sidebar.header("DataFrame Visualizer")
st.write(
    """This application highlights how `st.write` and `st.altair_chart` can be used 
to explore and visualize Pandas DataFrames. (Dataset provided by the 
[UN Data Explorer](http://data.un.org/Explorer.aspx).)"""
)

@st.cache_data
def load_agri_stats():
    """Downloads the UN agricultural dataset."""
    s3_url = "http://streamlit-demo-data.s3-us-west-2.amazonaws.com/agri.csv.gz"
    dataset = pd.read_csv(s3_url)
    return dataset.set_index("Region")

try:
    agri_df = load_agri_stats()
    
    # Country selection widget
    selected_nations = st.multiselect(
        "Select countries to compare", 
        list(agri_df.index), 
        default=["China", "United States of America"]
    )
    
    if not selected_nations:
        st.error("You must choose at least one country to proceed.")
    else:
        # Filter the data and convert values to billions
        filtered_stats = agri_df.loc[selected_nations]
        filtered_stats /= 1_000_000.0
        
        # Show raw table
        st.write("### Total Agricultural Production ($B)", filtered_stats.sort_index())

        # Pivot the dataframe for Altair plotting
        reshaped_df = filtered_stats.T.reset_index()
        reshaped_df = pd.melt(reshaped_df, id_vars=["index"]).rename(
            columns={"index": "year", "value": "Gross Agricultural Product ($B)"}
        )
        
        # Construct and render the Altair Area chart
        area_plot = (
            alt.Chart(reshaped_df)
            .mark_area(opacity=0.3)
            .encode(
                x="year:T",
                y=alt.Y("Gross Agricultural Product ($B):Q", stack=None),
                color="Region:N",
            )
        )
        st.altair_chart(area_plot, use_container_width=True)
        
except URLError as err:
    st.error(f"**Internet access is required to run this demo.**\n\nConnection error: {err.reason}")