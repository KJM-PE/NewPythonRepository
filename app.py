import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Generate a time series of 100 points where 2 is added at each point
time_series = np.cumsum(np.full(100, 2))

# Create a DataFrame for the time series
df = pd.DataFrame({
    'Point': range(1, 101),
    'Value': time_series
})

# Title of the app
st.title("Stuart is a loser...")

# Display the DataFrame
st.subheader("Time Series Data (First 100 Points)")
st.dataframe(df.iloc[:100, :2])

# Plotting the time series data using Matplotlib
st.subheader("Line Plot of Time Series")

# Using matplotlib to create the plot
fig, ax = plt.subplots()
ax.plot(df['Point'], df['Value'], marker='o', linestyle='-', color='b')
ax.set_title("Time Series with 2 Added Over 100 Points")
ax.set_xlabel("Point")
ax.set_ylabel("Value")
ax.grid(True)

# Display the plot in Streamlit
st.pyplot(fig)