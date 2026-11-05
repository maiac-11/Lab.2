# This creates the main landing page for the Streamlit application.
# Contains an introduction to the project and guide users to other pages.

# Import Streamlit
import streamlit as st

st.image("images/beach.png")

# st.set_page_config() is used to configure the page's appearance in the browser tab.
# It's good practice to set this as the first Streamlit command in your script.
st.set_page_config(
    page_title="Beach Cleanup Project",  # The title that appears in the browser tab
    page_icon="🏠",         # An emoji that appears as the icon in the browser tab
)

# WELCOME PAGE TITLE
st.title("Welcome to the Beach Cleanup Project! 📊")

# INTRODUCTORY TEXT
st.write("""
Our beaches and oceans are affected by pollution every day.
From plastic bottles to cigarette butts, trash can harm marine
life and damage coastal ecosystems.

This project collects information about beach pollution to help
us better understand the types of waste found along our beaches.
By collecting and visualizing data, we can identify common
pollutants and learn more about the impact of human activities
on our oceans.

### How to use this app:
- **Survey Page**: Go here to input new data into our CSV file.
- **Visuals Page**: Go here to see the data visualized in different graphs.

This project is part of CS 1301's Lab 2.
""")

# OPTIONAL: ADD AN IMAGE
# 1. Navigate to the 'images' folder in your Lab02 directory.
# 2. Place your image file (e.g., 'welcome_image.png') inside that folder.
# 3. Uncomment the line below and change the filename to match yours.
