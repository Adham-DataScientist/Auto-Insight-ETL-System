import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة والتصميم الفخم (Dark Professional Theme)
st.set_page_config(
    page_title="Universal Auto-Insight ETL System", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# تخصيص واجهة المستخدم بالـ CSS الاحترافي
st.markdown("""
    <style>
    /* تغيير لون الخلفية بالكامل */
    .stApp {
        background-color: #0B0F19;
        color: #E2E8F0;
    }
    /* تعديل الهيدر والعناوين */
    h1 {
        color: #00F2FE !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-weight: 700;
        text-shadow: 0px 0px 15px rgba(0, 242, 254, 0.3);
    }
    h3 {
        color: #94A3B8 !important;
        font-weight: 500;
    }
    /* تصميم كروت الـ KPIs الفخمة */
    div[data-testid="stMetric"] {
        background: linear-gradient(145deg, #1E293B, #0F172A);
        border-radius: 12px;
        padding: 20px 25px;
        border: 1px solid #334155;
        box-shadow: 0 4px 20px 0 rgba(0, 0, 0, 0.25);
        transition: transform 0.3s ease;
    }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-5px);
        border-color: #00F2FE;
    }
    /* تعديل نصوص الـ Metric */
    div[data-testid="stMetricLabel"] {
        color: #94A3B8 !important;
        font-size: 14px !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    div[data-testid="stMetricValue"] {
        color: #FFFFFF !important;
        font-size: 28px !important;
        font-weight: 600 !important;
    }
    /* تنسيق أزرار رفع الملفات والقوائم */
    .stSelectbox label, .stFileUploader label {
        color: #CBD5E1 !important;
        font-weight: 600;
    }
    /* خطوط الفصل */
    hr {
        border-color: #1E293B !important;
    }
    </style>
    """, unsafe_allow_html=True)

# الـ Sidebar الجانبي لإعطاء مظهر لوحة تحكم حقيقية
with st.sidebar:
    st.markdown("<h2 style='color: #00F2FE;'>🛠️ ETL Control Panel</h2>", unsafe_allow_html=True)
    st.write("Manage your uploaded data structures dynamically.")
    st.divider()
    st.markdown("🌐 **System Status:** `Active / Cloud-Ready`")
    st.markdown("👨‍💻 **Developer:** `Adham`")

# الواجهة الرئيسية
st.markdown("<h1>📊 Universal Auto-Insight ETL System</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #94A3B8; font-size: 16px;'>Transforming raw commercial datasets into interactive executive intelligence.</p>", unsafe_allow_html=True)
st.divider()

# 2. رفع الملف
uploaded_file = st.file_uploader("Upload your Enterprise Sales Data File", type=['xlsx', 'csv'])

if uploaded_file is not None:
    with st.spinner("⏳ Parsing enterprise architecture... Please wait..."):
        try:
            # قراءة الملف بأعلى كفاءة لـ 5000 سطر
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file, nrows=5000)
            else:
                df = pd.read_excel(uploaded_file, engine='openpyxl', nrows=5000)
                
            st.success(f"🚀 Deployment Successful: Loaded {df.shape[0]} rows across {df.shape[1]} operational features.")
            
            # عرض أول 5 أسطر بتنسيق منظم
            st.subheader("📑 Interactive Data Ledger")
            st.dataframe(df.head(5), use_container_width=True)
            
            st.divider()

            # ---- [إعدادات الفلترة الديناميكية] ----
            st.subheader("⚙️ Analytical Configuration")
            all_columns = df.columns.tolist()
            
            col_setup1, col_setup2, col_setup3 = st.columns(3)
            with col_setup1:
                category_col = st.selectbox("Categorical Pivot Point (X-Axis):", all_columns, index=0)
            with col_setup2:
                default_num_index = 1 if len(all_columns) > 1 else 0
                numeric_col = st.selectbox("Numerical Target Matrix (Y-Axis):", all_columns, index=default_num_index)
            with col_setup3:
                time_col = st.selectbox("Temporal Tracking Column (Optional Line Chart):", ["None"] + all_columns)

            st.divider()

            # ---- [تجهيز البيانات المنفصلة للحسابات] ----
            calc_col = "Cleaned_Amount"
            if df[numeric_col].dtype == 'object':
                df[calc_col] = df[numeric_col].astype(str).str.replace('$', '', regex=False).str.replace(',', '', regex=False).str.strip()
            else:
                df[calc_col] = df[numeric_col]
            df[calc_col] = pd.to_numeric(df[calc_col], errors='coerce').fillna(0)

            # ---- [عرض مؤشرات الأداء الحية KPIs] ----
            st.subheader("📈 Executive Metrics Overview")
            
            metric1, metric2, metric3 = st.columns(3)
            metric1.metric("Total Records", f"{len(df):,}")
            metric2.metric(f"Cumulative {numeric_col}", f"${df[calc_col].sum():,.2f}")
            metric3.metric(f"Mean Average Value", f"${df[calc_col].mean():,.2f}")

            st.divider()

            # ---- [الرسومات البيانية التفاعلية المنسقة] ----
            st.subheader("📊 Visual Intelligence Stream")
            chart_col1, chart_col2 = st.columns(2)
            
            with chart_col1:
                st.markdown(f"<p style='color: #00F2FE; font-weight: bold;'>Volume Distribution: {numeric_col} by {category_col}</p>", unsafe_allow_html=True)
                category_summary = df.groupby(category_col)[calc_col].sum().head(12)
                st.bar_chart(category_summary, color="#00F2FE") # تلوين التشارت بالنيون بلو
            
            with chart_col2:
                if time_col != "None":
                    st.markdown(f"<p style='color: #00F2FE; font-weight: bold;'>Temporal Trendline: {numeric_col} over {time_col}</p>", unsafe_allow_html=True)
                    time_summary = df.groupby(time_col)[calc_col].sum().head(25)
                    st.line_chart(time_summary, color="#FF007F") # تلوين الخط باللون الوردي المضيء
                else:
                    st.info("💡 Tip: Select a Time Column to unlock the Temporal Trendline graph inside this slot.")

            # ---- [محرك التنبؤ المبسط بالـ AI] ----
            st.divider()
            st.subheader("🤖 Predictive Intelligence Core")
            input_value = st.number_input(f"Calibrate baseline {numeric_col} entry for forecasting ($):", min_value=0, value=1000)
            
            st.markdown(
                f"""
                <div style='background-color: #1E1B4B; padding: 15px; border-radius: 8px; border-left: 5px solid #6366F1;'>
                    <span style='color: #C7D2FE;'>💡 <b>AI Forecast Output:</b> Estimated financial variance target for this baseline is <b>${input_value * 0.25:,.2f}</b></span>
                </div>
                """, 
                unsafe_allow_html=True
            )

        except Exception as e:
            st.error(f"❌ Structural Execution Error: {e}")
else:
    st.info("☝️ Awaiting file ingestion. Please upload an Excel or CSV file to initialize analysis.")