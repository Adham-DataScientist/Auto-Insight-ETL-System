import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة والتصميم
st.set_page_config(page_title="Universal Auto-Insight Dashboard", layout="wide")

st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    [data-testid='stMetric'] {
        background-color: #1e2130;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #2d3142;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("📊 Universal Auto-Insight ETL System")
st.markdown("Upload **any** sales dataset to extract instant business intelligence! 🚀")

# 2. رفع أي ملف إكسيل أو CSV
uploaded_file = st.file_uploader("Upload your Sales Data File", type=['xlsx', 'csv'])

if uploaded_file is not None:
    # قراءة الملف حسب صيغته ديناميكياً
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)
        
    st.success(f"✅ Successfully loaded '{uploaded_file.name}' with {df.shape[0]} rows and {df.shape[1]} columns!")
    st.divider()

    # عرض البيانات المرفوعة
    st.subheader("📑 Data Preview")
    st.dataframe(df.head(), use_container_width=True)
    
    st.divider()

    # ---- [مرحلة الفلترة والتحليل الديناميكي] ----
    st.subheader("⚙️ Configure Your Dashboard Columns")
    st.info("Please select which columns match your data features:")
    
    all_columns = df.columns.tolist()
    
    col_setup1, col_setup2, col_setup3 = st.columns(3)
    
    with col_setup1:
        # اختيار العمود النصي/الفئة (مثل الدولة، المنتج، أو الفرع)
        category_col = st.selectbox("Select Categorical Column (e.g., Country/Product):", all_columns)
    
    with col_setup2:
        # اختيار عمود المبيعات أو الأرباح الأساسي (رقمي)
        numeric_col = st.selectbox("Select Target Numeric Column (e.g., Profits/Sales):", all_columns)
        
    with col_setup3:
        # اختيار عمود الوقت أو التاريخ لو وُجد
        time_col = st.selectbox("Select Time/Date Column (Optional):", ["None"] + all_columns)

    # تحويل العمود الرقمي المختار إلى أرقام لضمان عدم حدوث خطأ
    df[numeric_col] = pd.to_numeric(df[numeric_col], errors='coerce').fillna(0)

    st.divider()

    # ---- [عرض المؤشرات بناءً على اختيار المستخدم] ----
    st.subheader("📈 Dynamic Business Insights")
    
    metric1, metric2 = st.columns(2)
    metric1.metric("Total Transactions (Rows)", f"{len(df):,}")
    metric2.metric(f"Total Combined {numeric_col}", f"${df[numeric_col].sum():,.2f}")

    st.write("") # مسافة تجميلية

    # ---- [الرسومات البيانية الديناميكية] ----
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        st.write(f"**Total {numeric_col} Distribution by {category_col}**")
        category_summary = df.groupby(category_col)[numeric_col].sum()
        st.bar_chart(category_summary)
    
    with chart_col2:
        if time_col != "None":
            st.write(f"**{numeric_col} Trends Over {time_col}**")
            time_summary = df.groupby(time_col)[numeric_col].sum()
            st.line_chart(time_summary)
        else:
            st.warning("⚠️ Select a Time Column to display the trend line chart.")

    # ---- [محرك التنبؤ الذكي المبسط] ----
    st.divider()
    st.subheader("🤖 Dynamic AI Predictor")
    st.write(f"Predict future {numeric_col} increments based on a baseline factor.")
    
    input_value = st.number_input(f"Enter baseline {numeric_col} value ($):", min_value=0, value=1000, step=100)
    
    # نسبة افتراضية للتنبؤ (يمكن تطويرها لموديل كامل لاحقاً)
    predicted_output = input_value * 0.25
    st.info(f"💡 Estimated future target output for **${input_value:,}**: **${predicted_output:,.2f}**")

else:
    st.info("☝️ Please upload an Excel or CSV file to start the automated analysis.")