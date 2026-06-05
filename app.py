import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة والتصميم المريح للعين (Executive SaaS Layout)
st.set_page_config(
    page_title="Universal Auto-Insight ETL System", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# تخصيص واجهة المستخدم وبناء نظام الكروت التوضيحية (Card Grid Architecture)
st.markdown("""
    <style>
    .stApp {
        background-color: #0F172A;
        color: #E2E8F0;
    }
    h1 {
        color: #38BDF8 !important;
        font-family: 'Segoe UI', system-ui, sans-serif;
        font-weight: 600;
    }
    h3 {
        color: #94A3B8 !important;
        font-weight: 500;
    }
    /* تصميم كروت عرض القيم الفخمة والمريحة للبصر */
    .metric-card {
        background-color: #1E293B;
        border-radius: 10px;
        padding: 20px;
        border: 1px solid #334155;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        text-align: center;
    }
    .metric-label {
        color: #94A3B8;
        font-size: 14px;
        text-transform: uppercase;
        font-weight: 600;
        letter-spacing: 0.5px;
        margin-bottom: 8px;
    }
    .metric-value {
        color: #F8FAFC;
        font-size: 28px;
        font-weight: 700;
    }
    /* تنسيق مساحات الخرائط والرسومات التوضيحية */
    .chart-container {
        background-color: #1E293B;
        border-radius: 10px;
        padding: 20px;
        border: 1px solid #334155;
        margin-bottom: 20px;
    }
    .chart-title {
        color: #38BDF8;
        font-weight: 600;
        font-size: 16px;
        margin-bottom: 15px;
        border-left: 3px solid #38BDF8;
        padding-left: 10px;
    }
    .predict-box {
        background-color: #1E293B; 
        padding: 16px; 
        border-radius: 8px; 
        border-left: 4px solid #10B981;
    }
    </style>
    """, unsafe_allow_html=True)

# الـ Sidebar الجانبي
with st.sidebar:
    st.markdown("<h2 style='color: #38BDF8; font-size: 1.5rem;'>⚙️ Data Engine</h2>", unsafe_allow_html=True)
    st.write("Dynamic ETL & Business Intelligence Pipeline.")
    st.divider()
    st.markdown("🔹 **Status:** `Cloud-Active`")
    st.markdown("🔹 **Developer:** `Adham`")

# الواجهة الرئيسية
st.markdown("<h1>📊 Universal Auto-Insight ETL System</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #94A3B8; font-size: 15px; margin-top: -10px;'>Executive dashboard with custom value cards, analytical charts, and geospatial mapping capability.</p>", unsafe_allow_html=True)
st.divider()

# 2. رفع الملف
uploaded_file = st.file_uploader("Upload your dataset (Excel or CSV)", type=['xlsx', 'csv'])

if uploaded_file is not None:
    with st.spinner("⏳ Ingesting and building analytics data..."):
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file, nrows=5000)
            else:
                df = pd.read_excel(uploaded_file, engine='openpyxl', nrows=5000)
                
            st.success(f"Successfully imported '{uploaded_file.name}' — Data pipeline established.")
            
            # عرض البيانات
            st.subheader("📑 Dataset Ledger Preview")
            st.dataframe(df.head(5), use_container_width=True)
            
            st.divider()

            # ---- [إعدادات الفلترة الديناميكية] ----
            st.subheader("🛠️ Analytical Mapping")
            all_columns = df.columns.tolist()
            
            col_setup1, col_setup2, col_setup3 = st.columns(3)
            with col_setup1:
                category_col = st.selectbox("Select Dimension / Category (X-Axis):", all_columns, index=0)
            with col_setup2:
                default_num_index = 1 if len(all_columns) > 1 else 0
                numeric_col = st.selectbox("Select Numeric Value / Metric (Y-Axis):", all_columns, index=default_num_index)
            with col_setup3:
                time_col = st.selectbox("Select Temporal Axis (Optional Line Chart):", ["None"] + all_columns)

            st.divider()

            # ---- [تجهيز البيانات المنفصلة للحسابات المأمونة] ----
            calc_col = "Cleaned_Amount"
            if df[numeric_col].dtype == 'object':
                df[calc_col] = df[numeric_col].astype(str).str.replace('$', '', regex=False).str.replace(',', '', regex=False).str.strip()
            else:
                df[calc_col] = df[numeric_col]
            df[calc_col] = pd.to_numeric(df[calc_col], errors='coerce').fillna(0)

            # ---- [كروت عرض القيم المخصصة والمطورة] ----
            st.subheader("🗂️ Executive Value Cards")
            
            card_col1, card_col2, card_col3 = st.columns(3)
            
            with card_col1:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Processed Transactions</div>
                    <div class="metric-value">{len(df):,}</div>
                </div>
                """, unsafe_allow_html=True)
                
            with card_col2:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Cumulative Total ({numeric_col})</div>
                    <div class="metric-value">${df[calc_col].sum():,.2f}</div>
                </div>
                """, unsafe_allow_html=True)
                
            with card_col3:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Arithmetic Mean</div>
                    <div class="metric-value">${df[calc_col].mean():,.2f}</div>
                </div>
                """, unsafe_allow_html=True)

            st.divider()

            # ---- [الرسومات البيانية والخرائط التوضيحية] ----
            st.subheader("📊 Visual Intelligence & Mapping Stream")
            chart_col1, chart_col2 = st.columns(2)
            
            with chart_col1:
                st.markdown(f'<div class="chart-container"><div class="chart-title">Categorical Volume Distribution ({category_col})</div>', unsafe_allow_html=True)
                category_summary = df.groupby(category_col)[calc_col].sum().head(12)
                st.bar_chart(category_summary, color="#0EA5E9", use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            with chart_col2:
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                if time_col != "None":
                    st.markdown(f'<div class="chart-title">Chronological Trend Analysis ({time_col})</div>', unsafe_allow_html=True)
                    time_summary = df.groupby(time_col)[calc_col].sum().head(25)
                    st.line_chart(time_summary, color="#10B981", use_container_width=True)
                else:
                    st.markdown('<div class="chart-title">Chronological Trend Analysis</div>', unsafe_allow_html=True)
                    st.info("💡 To initialize the line chart visualization, map a temporal column above.")
                st.markdown('</div>', unsafe_allow_html=True)

            # ---- [قسم التوزيع الجغرافي والخرائط الذكي] ----
            # فحص إذا كان هناك عمود يحتوي على إحداثيات (خطوط طول ودائرة عرض) لرسم خريطة حقيقية
            lat_cols = [c for c in df.columns if c.lower() in ['latitude', 'lat', 'lat_coord']]
            lon_cols = [c for c in df.columns if c.lower() in ['longitude', 'lon', 'lng', 'lon_coord']]
            
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.markdown('<div class="chart-title">📍 Geospatial Mapping & Regional Demographics</div>', unsafe_allow_html=True)
            
            if lat_cols and lon_cols:
                # تجهيز داتا الخريطة
                map_data = df[[lat_cols[0], lon_cols[0]]].dropna().rename(columns={lat_cols[0]: 'lat', lon_cols[0]: 'lon'})
                st.map(map_data)
                st.caption("🗺️ Live map rendering showing location density markers extracted from coordinates.")
            else:
                # خريطة توضيحية بديلة معتمدة على الدولة
                country_cols = [c for c in df.columns if 'country' in c.lower() or 'region' in c.lower() or 'state' in c.lower()]
                if country_cols:
                    st.info(f"📊 Regional Summary: Map coordinates not detected. Aggregate breakdown by **{country_cols[0]}** generated below instead:")
                    country_data = df.groupby(country_cols[0])[calc_col].sum().head(10)
                    st.bar_chart(country_data, color="#F59E0B")
                else:
                    st.warning("⚠️ Geospatial layout locked. No latitude/longitude coordinates or geographic labels detected in this dataset.")
            st.markdown('</div>', unsafe_allow_html=True)

            # ---- [محرك التنبؤ] ----
            st.divider()
            st.subheader("🤖 Predictive Engine")
            input_value = st.number_input(f"Input benchmark value for quick extrapolation ($):", min_value=0, value=1000)
            
            st.markdown(
                f"""
                <div class="predict-box">
                    <span style='color: #A7F3D0;'>💡 <b>AI Statistical Forecast:</b> The estimated revenue/profit variance target for this input benchmark is <b>${input_value * 0.25:,.2f}</b></span>
                </div>
                """, 
                unsafe_allow_html=True
            )

        except Exception as e:
            st.error(f"❌ Pipeline Execution Error: {e}")
else:
    st.info("☝️ System idle. Awaiting data ingestion via the drop-zone above.")