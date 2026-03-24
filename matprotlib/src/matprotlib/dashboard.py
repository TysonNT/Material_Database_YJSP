import streamlit as st
import pandas as pd
import numpy as np
import matprotlib as mp

# --- 1. Page Setup ---
st.set_page_config(page_title="Material Explorer", layout="wide")
st.title("🔬 MatProtLib: Interactive Database")

# --- 2. The Sidebar (User Inputs) ---
with st.sidebar:
    st.header("Control Panel")
    
    # Dropdown for Materials (automatically pulls from your database!)
    available_materials = mp.list_materials()
    selected_name = st.selectbox("Select Material", available_materials)
    
    # Fetch the chosen alloy
    alloy = mp.get_material(selected_name)
    
    # Dropdown for Properties (dynamically looks at what the alloy has)
    available_props = list(alloy.properties.keys())
    selected_prop = st.selectbox("Select Property", available_props)
    
    st.markdown("---")
    st.write(f"**Default Condition:** {alloy.default_condition}")

# --- 3. Data Processing (The Engine) ---
# We use your exact interpolation logic to generate 50 data points between 300K and 1200K
temps = np.linspace(300, 1200, 50)
values = [alloy.get(selected_prop, T=t) for t in temps]

# Put the data into a Pandas DataFrame so it's easy to graph and export
df = pd.DataFrame({
    "Temperature (K)": temps,
    selected_prop.replace("_", " ").title(): values
}).set_index("Temperature (K)")

# --- 4. Main View: Graph & Export ---
st.subheader(f"{selected_name.replace('_', ' ').title()} - {selected_prop.replace('_', ' ').title()}")

# Draw the interactive line chart
st.line_chart(df)

# The CSV Export Button
csv_data = df.to_csv().encode('utf-8')
st.download_button(
    label="📥 Export Data to CSV",
    data=csv_data,
    file_name=f"{selected_name}_{selected_prop}.csv",
    mime="text/csv",
)
