import streamlit as st
import joblib
import numpy as np
import pandas as pd
import time
import plotly.express as px
import plotly.graph_objects as go

# =========================
# Page Configuration
# =========================
st.set_page_config(
    page_title="🏠 Energy Efficiency Prediction",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =========================
# Load Machine Learning Model
# =========================
model = joblib.load("gradient_boosting_model.pkl")

# =========================
# Custom CSS
# =========================
st.markdown(
    """
<style>

.stApp{
    background-color:#F5F7FA;
}

h1,h2,h3{
    color:#0F172A;
}

[data-testid="stSidebar"]{
    background-color:#0F172A;
}

[data-testid="stSidebar"] *{
    color:white;
}

div[data-testid="metric-container"]{
    background-color:white;
    border-radius:15px;
    padding:20px;
    border-left:6px solid #2563EB;
    box-shadow:0 4px 12px rgba(0,0,0,.15);
}

.stButton>button{
    width:100%;
    height:55px;
    background:#2563EB;
    color:white;
    border:none;
    border-radius:10px;
    font-size:18px;
    font-weight:bold;
}

.stButton>button:hover{
    background:#1D4ED8;
}

.hero{
    background:linear-gradient(90deg,#2563EB,#0EA5E9);
    padding:30px;
    border-radius:15px;
    color:white;
    margin-bottom:25px;
}

.footer{
    text-align:center;
    color:gray;
    margin-top:40px;
}

</style>
""",
    unsafe_allow_html=True,
)

# =========================
# Sidebar
# =========================
with st.sidebar:

    st.image(
        "https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=900",
        use_container_width=True,
    )

    st.title("🏠 Energy AI")

    st.markdown("---")

    st.success("✔ Gradient Boosting Regressor")

    st.info("""
This application predicts:

🔥 Heating Load

❄ Cooling Load

using Machine Learning.
""")

    st.markdown("---")

    st.write("### 📌 Project Features")

    st.write("✅ Machine Learning")

    st.write("✅ Energy Prediction")

    st.write("✅ Smart Buildings")

    st.write("✅ Interactive Dashboard")

# =========================
# Hero Section
# =========================
st.markdown(
    """
<div class="hero">

<h1>🏠 Energy Efficiency Prediction System</h1>

<p style="font-size:18px">

Predict the Heating Load and Cooling Load of residential
buildings using Artificial Intelligence and Machine Learning.

</p>

</div>
""",
    unsafe_allow_html=True,
)

# =========================
# Project Description
# =========================
left, right = st.columns([2, 1])

with left:

    st.subheader("📖 About the Project")

    st.write("""
Energy consumption is one of the most important challenges in modern buildings.

This application predicts:

• 🔥 Heating Load

• ❄ Cooling Load

using a trained Gradient Boosting Regressor Model.

The goal is to help engineers design more energy-efficient buildings.
""")

with right:

    st.image(
        "https://images.unsplash.com/photo-1511818966892-d7d671e672a2?w=800",
        use_container_width=True,
    )

st.divider()
# =========================
# Building Features
# =========================

st.subheader("🏗 Building Features")

st.info("Fill in the building information below, then press Predict.")

with st.form("prediction_form"):

    col1, col2 = st.columns(2)

    with col1:

        relative_compactness = st.number_input(
            "🏠 Relative Compactness",
            min_value=0.50,
            max_value=1.00,
            value=0.80,
            step=0.01,
        )

        surface_area = st.number_input(
            "📐 Surface Area",
            min_value=400.0,
            value=600.0,
            step=1.0,
        )

        wall_area = st.number_input(
            "🧱 Wall Area",
            min_value=200.0,
            value=300.0,
            step=1.0,
        )

        roof_area = st.number_input(
            "🏡 Roof Area",
            min_value=100.0,
            value=150.0,
            step=1.0,
        )

    with col2:

        overall_height = st.number_input(
            "🏢 Overall Height",
            min_value=3.0,
            value=7.0,
            step=0.5,
        )

        orientation = st.selectbox("🧭 Orientation", [2, 3, 4, 5])

        glazing_area = st.selectbox("🪟 Glazing Area", [0.00, 0.10, 0.25, 0.40])

        glazing_distribution = st.selectbox(
            "🌞 Glazing Distribution", [0, 1, 2, 3, 4, 5]
        )

    st.markdown("")

    predict = st.form_submit_button("🚀 Predict Energy Consumption")
    # =========================
# Prediction
# =========================

if predict:

    with st.spinner("🤖 AI Model is predicting..."):
        time.sleep(1)

        data = np.array(
            [
                [
                    relative_compactness,
                    surface_area,
                    wall_area,
                    roof_area,
                    overall_height,
                    orientation,
                    glazing_area,
                    glazing_distribution,
                ]
            ]
        )

        prediction = model.predict(data)

    # استخراج النتائج
    try:
        heating = float(prediction[0][0])
        cooling = float(prediction[0][1])
    except:
        heating = float(prediction[0])
        cooling = 0.0

    st.success("✅ Prediction Completed Successfully!")

    st.markdown("## 📊 Prediction Results")

    c1, c2 = st.columns(2)

    with c1:
        st.metric(label="🔥 Heating Load", value=f"{heating:.2f} kWh/m²")

    with c2:
        st.metric(label="❄ Cooling Load", value=f"{cooling:.2f} kWh/m²")

    st.markdown("---")

    # رسم بياني احترافي
    chart_df = pd.DataFrame(
        {"Type": ["Heating Load", "Cooling Load"], "Value": [heating, cooling]}
    )

    fig = px.bar(
        chart_df,
        x="Type",
        y="Value",
        color="Type",
        text="Value",
        title="Energy Load Comparison",
    )

    fig.update_traces(texttemplate="%{text:.2f}", textposition="outside")

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    average = (heating + cooling) / 2

    st.subheader("🏆 Building Efficiency")

    if average < 20:
        st.success("🟢 Excellent Energy Efficiency")
        st.progress(95)

    elif average < 35:
        st.warning("🟡 Good Energy Efficiency")
        st.progress(70)

    else:
        st.error("🔴 Poor Energy Efficiency")
        st.progress(40)

    st.markdown("---")

    st.subheader("📋 Building Summary")

    summary = pd.DataFrame(
        {
            "Feature": [
                "Relative Compactness",
                "Surface Area",
                "Wall Area",
                "Roof Area",
                "Overall Height",
                "Orientation",
                "Glazing Area",
                "Glazing Distribution",
            ],
            "Value": [
                relative_compactness,
                surface_area,
                wall_area,
                roof_area,
                overall_height,
                orientation,
                glazing_area,
                glazing_distribution,
            ],
        }
    )

    st.dataframe(summary, use_container_width=True)
    # =========================
# About Project
# =========================

st.markdown("---")

tab1, tab2, tab3 = st.tabs(["📖 About Project", "🤖 Machine Learning", "👨‍💻 Team"])

# =========================
# About
# =========================

with tab1:

    st.subheader("Energy Efficiency Prediction")

    st.write("""
This project predicts the Heating Load and Cooling Load
for residential buildings using Machine Learning.

The model was trained on the Energy Efficiency Dataset
to estimate the energy required for heating and cooling.

The application aims to help engineers design
energy-efficient buildings.
""")

    st.info("""
Dataset Features

• Relative Compactness

• Surface Area

• Wall Area

• Roof Area

• Overall Height

• Orientation

• Glazing Area

• Glazing Area Distribution
""")

# =========================
# ML
# =========================

with tab2:

    st.subheader("Machine Learning Model")

    st.write("""
Algorithm Used:

✅ Gradient Boosting Regressor

Libraries:

• Scikit-learn

• Pandas

• NumPy

• Streamlit

• Plotly

The model predicts the building energy loads
based on architectural characteristics.
""")

# =========================
# Team
# =========================

# =========================
# Team
# =========================

with tab3:

    st.subheader("👨‍💻 Project Team")

    st.info("""
**NTI Machine Learning Project**

Team Members:
""")

    col1, col2 = st.columns(2)

    with col1:
        st.success("""
👩 Habiba Gamal

👨 Abdelwahab Ali

👩 Shahd Shawkat
""")

    with col2:
        st.success("""
👨 Amir Mustafa

👩 Eman Abo Al Qassem
""")
# =========================
# Footer
# =========================

st.markdown(
    """
<div style='text-align:center; color:gray;'>

<h3>🏠 Energy Efficiency Prediction System</h3>

<p><b>NTI Machine Learning Project</b></p>

<p>Developed by</p>

<p>
Habiba Gamal • Abdelwahab Ali • Shahd Shawkat • Amir Mustafa • Eman Abo Al Qassem
</p>

<p>Built with ❤️ using Streamlit, Scikit-learn & Plotly</p>

</div>
""",
    unsafe_allow_html=True,
)
# =========================
# Dashboard Statistics
# =========================

if "heating" in locals() and "cooling" in locals():

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("📈 Energy Distribution")

        fig = go.Figure(
            data=[
                go.Pie(
                    labels=["Heating Load", "Cooling Load"],
                    values=[heating, cooling],
                    hole=0.55,
                )
            ]
        )

        fig.update_layout(height=420)

        st.plotly_chart(fig, use_container_width=True)

    with col2:

        st.subheader("⚡ Building Score")

        score = max(0, min(100, 100 - average))

        gauge = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=score,
                title={"text": "Efficiency Score"},
                gauge={
                    "axis": {"range": [0, 100]},
                    "bar": {"color": "green"},
                    "steps": [
                        {"range": [0, 40], "color": "#ffb3b3"},
                        {"range": [40, 70], "color": "#ffe699"},
                        {"range": [70, 100], "color": "#b6fcb6"},
                    ],
                },
            )
        )

        gauge.update_layout(height=420)

        st.plotly_chart(gauge, use_container_width=True)

    st.markdown("---")
