import streamlit as st
import pandas as pd
import joblib

# 1. Page Configuration
st.set_page_config(page_title="Building Energy Efficiency Predictor", layout="centered")
st.title("⚡ Building Energy Efficiency Predictor")
st.write("Enter the building parameters below to predict Heating and Cooling loads.")

# 2. Load the trained models
@st.cache_resource
def load_models():
    return joblib.load("gradient_boosting_models.pkl")

models = load_models()

# 3. Create User Inputs in the Sidebar or Main Page
st.sidebar.header("Building Features")

# Using typical ranges from the Energy Efficiency dataset
rel_compactness = st.sidebar.number_input("Relative Compactness", min_value=0.5, max_value=1.0, value=0.75, step=0.01)
surface_area = st.sidebar.number_input("Surface Area", min_value=500.0, max_value=900.0, value=650.0, step=1.0)
wall_area = st.sidebar.number_input("Wall Area", min_value=200.0, max_value=500.0, value=300.0, step=1.0)
roof_area = st.sidebar.number_input("Roof Area", min_value=100.0, max_value=250.0, value=150.0, step=1.0)
overall_height = st.sidebar.selectbox("Overall Height", options=[3.5, 7.0])
orientation = st.sidebar.selectbox("Orientation", options=[2, 3, 4, 5], help="2:North, 3:East, 4:South, 5:West")
glazing_area = st.sidebar.number_input("Glazing Area", min_value=0.0, max_value=0.5, value=0.25, step=0.05)
glazing_distribution = st.sidebar.selectbox("Glazing Area Distribution", options=[0, 1, 2, 3, 4, 5])

# 4. Format inputs into a DataFrame that matches x_train
input_data = pd.DataFrame({
    'Relative Compactness': [rel_compactness],
    'Surface Area': [surface_area],
    'Wall Area': [wall_area],
    'Roof Area': [roof_area],
    'Overall Height': [overall_height],
    'Orientation': [orientation],
    'Glazing Area': [glazing_area],
    'Glazing Area Distribution': [glazing_distribution]
})

st.subheader("Current Input Data")
st.dataframe(input_data, hide_index=True)

# 5. Make Predictions
if st.button("Predict Energy Loads", type="primary"):
    # Access the two separate models from the dictionary
    heating_model = models['Heating Load']
    cooling_model = models['Cooling Load']
    
    # Predict
    pred_heating = heating_model.predict(input_data)[0]
    pred_cooling = cooling_model.predict(input_data)[0]
    
    # Display Results visually
    st.subheader("Prediction Results")
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric(label="🔥 Heating Load", value=f"{pred_heating:.2f} kWh/m²")
        
    with col2:
        st.metric(label="❄️ Cooling Load", value=f"{pred_cooling:.2f} kWh/m²")