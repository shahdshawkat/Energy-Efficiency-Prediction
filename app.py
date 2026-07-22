import streamlit as st
import pandas as pd
import joblib
import numpy as np

# إعداد واجهة الصفحة
st.set_page_config(page_title="Building Energy Predictor", page_icon="🏠", layout="centered")

st.title("🏠 توقع أحمال التدفئة والتبريد للمباني")
st.markdown("قم بإدخال خصائص المبنى أدناه وسيقوم موديل **Random Forest** بحساب الأحمال المتوقعة.")

# دالة لتحميل الموديل مرة واحدة فقط لضمان سرعة التطبيق
@st.cache_resource
def load_model():
    return joblib.load("random_forest_model.pkl")

# محاولة تحميل الموديل
try:
    model = load_model()
except FileNotFoundError:
    st.error("⚠️ لم يتم العثور على ملف الموديل 'random_forest_model.pkl'. تأكد من وجوده في نفس المجلد.")
    st.stop()

st.divider()

# إنشاء عمودين لترتيب المدخلات بشكل أنيق
col1, col2 = st.columns(2)

with col1:
    st.subheader("أبعاد المبنى")
    rc = st.number_input("Relative Compactness", min_value=0.6, max_value=1.0, value=0.75, step=0.01)
    sa = st.number_input("Surface Area", min_value=500.0, max_value=850.0, value=670.0, step=1.0)
    wa = st.number_input("Wall Area", min_value=240.0, max_value=420.0, value=318.5, step=1.0)
    ra = st.number_input("Roof Area", min_value=110.0, max_value=230.0, value=147.0, step=1.0)

with col2:
    st.subheader("تفاصيل إضافية")
    oh = st.number_input("Overall Height", min_value=3.0, max_value=8.0, value=7.0, step=0.5)
    orientation = st.selectbox("Orientation (2:North, 3:East, 4:South, 5:West)", options=[2, 3, 4, 5])
    ga = st.selectbox("Glazing Area", options=[0.0, 0.1, 0.25, 0.40])
    gad = st.selectbox("Glazing Area Distribution", options=[0, 1, 2, 3, 4, 5])

st.divider()

# زر التوقع
if st.button("احسب الأحمال 🚀", use_container_width=True):
    
    # تجميع المدخلات في DataFrame بنفس أسماء الأعمدة المستخدمة في x_train
    input_data = pd.DataFrame([[rc, sa, wa, ra, oh, orientation, ga, gad]], 
                              columns=[
                                  'Relative Compactness', 
                                  'Surface Area', 
                                  'Wall Area', 
                                  'Roof Area', 
                                  'Overall Height', 
                                  'Orientation', 
                                  'Glazing Area', 
                                  'Glazing Area Distribution'
                              ])
    
    # إجراء التنبؤ
    prediction = model.predict(input_data)
    
    # الموديل يتوقع قيمتين [Heating Load, Cooling Load]
    heat_load = prediction[0][0]
    cool_load = prediction[0][1]
    
    # عرض النتائج
    res_col1, res_col2 = st.columns(2)
    with res_col1:
        st.success(f"🔥 **Heating Load:**\n# {heat_load:.2f}")
    with res_col2:
        st.info(f"❄️ **Cooling Load:**\n# {cool_load:.2f}")