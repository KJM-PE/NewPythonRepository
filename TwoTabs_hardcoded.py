install openai

import os

# Access the API key from environment variables
api_key_str = os.getenv("OPENAI_API_KEY")

from openai import OpenAI
client = OpenAI(api_key=api_key_str)


import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests
from io import BytesIO

# Set the title of the Streamlit app
st.title("Excel Data Loader and Plotter")

# Create two tabs: "Input URL" and "Data & Plot"
tab1, tab2, tab3 = st.tabs(["Data & Plot", "GPT Analysis", "Underlying Excel Link"])

# Initialize variables to store the URL and DataFrame across both tabs
uploaded_df = None


# Input field for GitHub raw URL
github_url = "https://github.com/KJM-PE/NewPythonRepository/raw/refs/heads/master/data.xlsx"
    
if github_url:
        try:
            # Fetch the Excel file from the provided URL
            response = requests.get(github_url)

            # Check if the response was successful
            if response.status_code == 200:
                file_bytes = BytesIO(response.content)
                uploaded_df = pd.read_excel(file_bytes, engine='openpyxl')  # Specify the engine explicitly
            else:
                st.error("Failed to fetch the file. Please check the URL.")
        
        except Exception as e:
            st.error(f"An error occurred while loading the file: {e}")

dataframe_text = uploaded_df.to_string(index=False)

# Create the prompt for GPT
prompt = f"""
I have the following data in a dataframe format:
{dataframe_text}

Can you please provide an analysis of this data, tell me if the data is changing?
"""

# Make a request to the OpenAI API to generate a response
response = client.chat.completions.create(model="gpt-4o",  # or 'gpt-4' if you have access
messages=[
    {"role": "system", "content": "You are a data analysis assistant."},
    {"role": "user", "content": prompt}
],
max_tokens=500)

chatresult_string=response.choices[0].message.content.strip()


# Tab 2: Show the table and plot
with tab1:
    st.header("Step 1: View Data and Plot")

    # If the DataFrame is available, display the data and plot
    if uploaded_df is not None:
        # Display the first few rows of the DataFrame
        st.write("Data from the Excel sheet:")
        st.write(uploaded_df.head())

        # Select columns for plotting
        if len(uploaded_df.columns) >= 2:
            x_axis = st.selectbox("Select X-axis", uploaded_df.columns)
            y_axis = st.selectbox("Select Y-axis", uploaded_df.columns)

            # Plot the selected columns
            if st.button("Plot Data"):
                plt.figure(figsize=(10, 5))
                plt.plot(uploaded_df[x_axis], uploaded_df[y_axis], marker='o')
                plt.xlabel(x_axis)
                plt.ylabel(y_axis)
                plt.title(f'{y_axis} vs {x_axis}')
                plt.grid(True)

                # Show the plot in Streamlit
                st.pyplot(plt.gcf())
        else:
            st.war

with tab2:
    st.header("Step 2: GPT Analysis")

    st.write(chatresult_string)

with tab3:
    st.header("Step 3: GitHub URL used")

    st.write(github_url)
