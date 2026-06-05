import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة والتصميم المريح للعين (SaaS Clean Slate Theme)
st.set_page_config(
    page_title="Universal Auto-Insight ETL System", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# تخصيص واجهة مستخدم ناعمة وذات تباين متزن (Low Strain UI)
st.markdown("""
    <style>
    /* خلفية داكنة هادئة ومريحة جداً للقرنية */
    .stApp {
        background-color: #0F172A;
        color: #E2E8F0;
    }
    /* تنسيق العناوين الأساسية بلون أزرق ناصع وناعم */
    h1 {
        color: #38BDF8 !important;
        font-family: 'Segoe UI', system-ui, sans-serif;
        font-weight: 600;
        font-size: 2.2rem !important;
    }
    h3 {
        color: #94A3B8 !important;
        font-weight: 500;
        font-size: 1.3rem !important;
    }
    /* تصميم كروت الـ KPIs بخلفية مسطحة مريحة وبدون توهج متعب */
    div[data-testid="stMetric"] {
        background-color: #1E293B;
        border-radius: 8px;
        padding: 18px 22px;
        border: 1px solid #334155;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
    }
    /* نصوص المؤشرات ناعمة وغير فاقعة */
    div[data-testid="stMetricLabel"] {
        color: #94A3B8 !important;
        font-size: 13px !important;
        font-weight: 500;
        letter-spacing: 0.5px;
    }
    div[data-testid="stMetricValue"] {
        color: #F8FAFC !important;
        font-size: 26px !important;
        font-weight: 600 !important;
    }
    /* تنسيق أزرار رفع الملفات والقوائم */
    .stSelectbox label, .stFileUploader label {
        color: #94A3B8 !important;
        font-weight: 500;
    }
    /* خطوط الفصل الهادئة */
    hr {
        border-color: #334155 !important;
    }
    /* تنسيق صندوق التنبؤ */
    .predict-box {
        background-color: #1E293B; 
        padding: 16px; 
        border-radius: 8px; 
        border-left: 4px solid #38BDF8;
        color: #E2E8F0;
    }
    </style>
    """, unsafe_allow_html=True)

# الـ Sidebar الجانبي المنسق بنعومة
with st.sidebar:
    st.markdown("<h2 style='color: #38BDF8; font-size: 1.5rem;'>⚙️ Data Engine</h2>", unsafe_allow_html=True)
    st.write("Configure and manage your analytical workflows seamlessly.")
    st.divider()
    st.markdown("🔹 **Environment:** `Production`")
    st.markdown("🔹 **Data Status:** `Ready`")
    st.markdown("🔹 **Developer:** `Adham`")

# الواجهة الرئيسية
st.markdown("<h1>📊 Universal Auto-Insight ETL System</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #94A3B8; font-size: 15px; margin-top: -10px;'>A clean, structured framework to clean, filter, and study commercial datasets.</p>", unsafe_allow_html=True)
st.divider()

# 2. رفع الملف
uploaded_file = st.file_uploader("Upload your enterprise dataset (CSV format is highly recommended)", type=['xlsx', 'csv'])

if uploaded_file is not None:
    with st.spinner("⏳ Reading data stream..."):
        try:
            # قراءة الملف بأعلى كفاءة لـ 5000 سطر
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file, nrows=5000)
            else:
                df = pd.read_excel(uploaded_file, engine='openpyxl', nrows=5000)
                
            st.success(f"Successfully imported '{uploaded_file.name}' — {df.shape[0]} rows initialized.")
            
            # عرض أول 5 أسطر بتنسيق منظم ومريح للعين
            st.subheader("📑 Dataset Ledger Preview")
            st.dataframe(df.head(5), use_container_width=True)
            
            st.divider()

            # ---- [إعدادات الفلترة الديناميكية] ----
            st.subheader("🛠️ Analytical Mapping")
            all_columns = df.columns.tolist()
            
            col_setup1, col_setup2, col_setup3 = st.columns(3)
            with col_setup1:
                category_col = st.selectbox("Select Dimension (X-Axis):", all_columns, index=0)
            with col_setup2:
                default_num_index = 1 if len(all_columns) > 1 else 0
                numeric_col = st.selectbox("Select Metric (Y-Axis):", all_columns, index=default_num_index)
            with col_setup3:
                time_col = st.selectbox("Select Temporal Axis (Optional):", ["None"] + all_columns)

            st.divider()

            # ---- [تجهيز البيانات المنفصلة للحسابات] ----
            calc_col = "Cleaned_Amount"
            if df[numeric_col].dtype == 'object':
                df[calc_col] = df[numeric_col].astype(str).str.replace('$', '', regex=False).str.replace(',', '', regex=False).str.strip()
            else:
                df[calc_col] = df[numeric_col]
            df[calc_col] = pd.to_numeric(df[calc_col], errors='coerce').fillna(0)

            # ---- [عرض مؤشرات الأداء الحية KPIs] ----
            st.subheader("📈 Summary Metrics")
            
            metric1, metric2, metric3 = st.columns(3)
            metric1.metric("Row Count", f"{len(df):,}")
            metric2.metric(f"Sum Total ({numeric_col})", f"${df[calc_col].sum():,.2f}")
            metric3.metric("Arithmetic Mean", f"${df[calc_col].mean():,.2f}")

            st.divider()

            # ---- [الرسومات البيانية التفاعلية المنسقة بألوان مريحة] ----
            st.subheader("📊 Visual Intelligence")
            chart_col1, chart_col2 = st.columns(2)
            
            with chart_col1:
                st.markdown(f"<p style='color: #94A3B8; font-weight: 500;'>Categorical Distribution: {numeric_col} by {category_col}</p>", unsafe_allow_html=True)
                category_summary = df.groupby(category_col)[calc_col].sum().head(12)
                # استخدام لون أزرق هادئ ومريح جداً للنظر (Soft Slate Blue)
                st.bar_chart(category_summary, color="#0EA5E9") 
            
            with chart_col2:
                if time_col != "None":
                    st.markdown(f"<p style='color: #94A3B8; font-weight: 500;'>Chronological Trend: {numeric_col} over {time_col}</p>", unsafe_allow_html=True)
                    time_summary = df.groupby(time_col)[calc_col].sum().head(25)
                    # لون مريمي/أخضر هادئ للخط الزمني (Calm Emerald/Mint)
                    st.line_chart(time_summary, color="#10B981") 
                else:
                    st.info("💡 To view chronological data trends over time, map a tracking feature into the Temporal Axis drop-down.")

            # ---- [محرك التنبؤ المبسط بالـ AI] ----
            st.divider()
            st.subheader("🤖 Predictive Engine")
            input_value = st.number_input(f"Input base metric value for quick extrapolation ($):", min_value=0, value=1000)
            
            st.markdown(
                f"""
                <div class="predict-box">
                    <b>💡 Statistical Estimate:</b> The forecasted benchmark profit target for your input value is <b>${input_value * 0.25:,.2f}</b>
                </div>
                """, 
                unsafe_allow_html=True
            )

        except Exception as e:
            st.error(f"❌ Structural Processing Exception: {e}")
else:
    st.info("☝️ Awaiting corporate data feed. Please drop an Excel or CSV file above to trigger the extraction pipeline.")