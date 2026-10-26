import streamlit as st
import pydeck as pdk

# Configure the main landing page
st.set_page_config(page_title="Home", page_icon="👋")

st.write("# Greetings from Streamlit! 👋")

# Display a hint in the sidebar
st.sidebar.success("Pick a demo from the menu above.")

st.markdown(
    """
    Streamlit is a powerful open-source framework designed specifically for 
    Data Science and Machine Learning web apps.
    **👈 Choose a demo in the sidebar** to explore some interactive 
    examples showcasing Streamlit's capabilities!
    
    ### Eager to learn more?
    - Visit our official site: [streamlit.io](https://streamlit.io)
    - Read through the [documentation](https://docs.streamlit.io)
    - Engage with the community on our [forums](https://discuss.streamlit.io)
    
    ### Explore advanced examples
    - Analyze the Udacity Self-driving Car Image Dataset with a neural network [here](https://github.com/streamlit/demo-self-driving)
    - Discover insights in a [NYC rideshare dataset](https://github.com/streamlit/demo-uber-nyc-pickups)
    """
)