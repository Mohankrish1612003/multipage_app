import streamlit as st
import time
import numpy as np

# Page configuration
st.set_page_config(page_title="Live Plotting", page_icon="📈")

st.markdown("# Live Plotting Demonstration")
st.sidebar.header("Live Plotting Demo")
st.write(
    """This application showcases how to combine real-time animations with 
Streamlit charts. We are generating random data points in a loop for about 
5 seconds. Sit back and watch!"""
)

# Initialize UI components for the animation
prog_bar = st.sidebar.progress(0)
status_msg = st.sidebar.empty()

# Set up initial random data and chart
chart_data = np.random.randn(1, 1)
line_plot = st.empty()
line_plot.line_chart(chart_data)

# Run the animation loop
for step in range(1, 101):
    # Generate new rows and append to our array
    appended_rows = chart_data[-1, :] + np.random.randn(5, 1).cumsum(axis=0)
    chart_data = np.concatenate([chart_data, appended_rows])
    
    # Update the UI elements
    status_msg.text(f"{step}% Finished")
    line_plot.line_chart(chart_data)
    prog_bar.progress(step)
    
    # Pause briefly to create the animation effect
    time.sleep(0.05)

# Clear the progress bar once complete
prog_bar.empty()

# Trigger a script rerun to play the animation again
st.button("Run Again")