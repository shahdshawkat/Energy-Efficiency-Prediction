import streamlit as st
import pandas as pd
import joblib

# 1. Page Configuration
st.set_page_config(
    page_title="Building Energy Predictor", 
    page_icon="🏢", 
    layout="centered"
)

# 2. Main Header
st.title("🏢 Building Energy Efficiency Predictor")
st.markdown("Enter the building characteristics below to predict the **Heating** and **Cooling** loads.")
st.divider()

# 3. Load the Model
@st.cache_resource
def load_model():
    return joblib.load("random_forest_model.pkl")

try:
    model = load_model()
except FileNotFoundError:
    st.error("⚠️ Model file 'random_forest_model.pkl' not found. Please ensure it is in the same directory.")
    st.stop()

# 4. Input Form (Using Number Inputs directly on the main page)
st.subheader("📐 Building Parameters")

# Creating two columns for a cleaner layout
col1, col2 = st.columns(2)

with col1:
    rc = st.number_input("Relative Compactness", min_value=0.60, max_value=1.00, value=0.75, step=0.01)
    sa = st.number_input("Surface Area", min_value=500.0, max_value=850.0, value=670.0, step=10.0)
    wa = st.number_input("Wall Area", min_value=240.0, max_value=420.0, value=318.5, step=5.0)
    ra = st.number_input("Roof Area", min_value=110.0, max_value=230.0, value=147.0, step=5.0)

with col2:
    oh = st.number_input("Overall Height", min_value=3.0, max_value=8.0, value=7.0, step=0.5)
    orientation = st.selectbox("Orientation", options=[2, 3, 4, 5], format_func=lambda x: f"{x} ({ {2: 'North', 3: 'East', 4: 'South', 5: 'West'}[x] })")
    ga = st.selectbox("Glazing Area", options=[0.0, 0.1, 0.25, 0.40])
    gad = st.selectbox("Glazing Area Distribution", options=[0, 1, 2, 3, 4, 5])

st.divider()

# 5. Prediction Button
predict_button = st.button("Predict Loads ⚡", use_container_width=True, type="primary")

# 6. Prediction Logic
if predict_button:
    # Prepare input data
    input_data = pd.DataFrame([[rc, sa, wa, ra, oh, orientation, ga, gad]], 
                              columns=[
                                  'Relative Compactness', 'Surface Area', 'Wall Area', 
                                  'Roof Area', 'Overall Height', 'Orientation', 
                                  'Glazing Area', 'Glazing Area Distribution'
                              ])
    
    # Predict using the loaded model
    prediction = model.predict(input_data)
    heat_load = prediction[0][0]
    cool_load = prediction[0][1]
    
    # Display Results Display
    st.subheader("📊 Prediction Results")
    
    res_col1, res_col2 = st.columns(2)
    with res_col1:
        st.metric(label="🔥 Heating Load", value=f"{heat_load:.2f}", delta="kWh/m²", delta_color="off")
    with res_col2:
        st.metric(label="❄️ Cooling Load", value=f"{cool_load:.2f}", delta="kWh/m²", delta_color="off")