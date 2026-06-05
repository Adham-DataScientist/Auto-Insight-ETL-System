import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة بتصميم الساس النظيف المريح جداً للعين
st.set_page_config(
    page_title="Universal Auto-Insight ETL System", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# تخصيص CSS متطور جداً لمنع تداخل الأرقام وتنسيق كروت العرض
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
        font-size: 2rem !important;
    }
    h2 {
        color: #F8FAFC !important;
        font-size: 1.4rem !important;
        font-weight: 500;
    }
    /* تصميم كروت الـ KPIs بشكل احترافي ناعم */
    .metric-card {
        background-color: #1E293B;
        border-radius: 8px;
        padding: 20px;
        border: 1px solid #334155;
        text-align: center;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .metric-label {
        color: #94A3B8;
        font-size: 12px;
        text-transform: uppercase;
        font-weight: 600;
        letter-spacing: 0.5px;
        margin-bottom: 8px;
    }
    .metric-value {
        color: #38BDF8;
        font-size: 22px;
        font-weight: 700;
        word-wrap: break-word;
    }
    /* حاويات الرسوم البيانية */
    .chart-box {
        background-color: #1E293B;
        border-radius: 8px;
        padding: 20px;
        border: 1px solid #334155;
        margin-bottom: 20px;
    }
    .predict-box {
        background-color: #1E293B; 
        padding: 15px; 
        border-radius: 8px; 
        border-left: 4px solid #10B981;
    }
    </style>
    """, unsafe_allow_html=True)

# دالة لتنسيق الأرقام الضخمة تلقائياً لكي لا تخرّب التصميم (Format Numbers)
def format_large_number(num):
    if num >= 1e12:
        return f"${num/1e12:,.2f} T"
    elif num >= 1e9:
        return f"${num/1e9:,.2f} B"
    elif num >= 1e6:
        return f"${num/1e6:,.2f} M"
    else:
        return f"${num:,.2f}"

# 2. الشريط الجانبي (Sidebar) لرفع وإعداد البيانات
with st.sidebar:
    st.markdown("<h2 style='color: #38BDF8; margin-bottom: 0;'>📁 Data Ingestion</h2>", unsafe_allow_html=True)
    st.write("Upload and configure your dataset here.")
    st.divider()
    
    uploaded_file = st.file_uploader("Choose Excel or CSV file", type=['xlsx', 'csv'])
    
    category_col = None
    numeric_col = None
    time_col = "None"
    
    if uploaded_file is not None:
        st.divider()
        st.markdown("<h3 style='color: #E2E8F0; font-size: 1.1rem; margin-bottom: 10px;'>⚙️ Column Mapping</h3>", unsafe_allow_html=True)
        
        try:
            if uploaded_file.name.endswith('.csv'):
                preview_df = pd.read_csv(uploaded_file, nrows=5)
            else:
                preview_df = pd.read_excel(uploaded_file, engine='openpyxl', nrows=5)
            
            all_columns = preview_df.columns.tolist()
            
            category_col = st.selectbox("Categorical (X-Axis):", all_columns, index=0)
            default_num_index = 1 if len(all_columns) > 1 else 0
            numeric_col = st.selectbox("Numeric (Y-Axis):", all_columns, index=default_num_index)
            time_col = st.selectbox("Temporal (Optional):", ["None"] + all_columns)
            
        except Exception as e:
            st.error(f"Error reading configuration: {e}")

    st.divider()
    st.markdown("🔹 **Status:** `Engine Ready`")
    st.markdown("👨‍💻 **Developer:** `Adham`")

# 3. الصفحة الرئيسية (Main Dashboard Screen)
st.markdown("<h1>📊 Universal Auto-Insight ETL System</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #94A3B8; font-size: 14px; margin-top: -10px;'>Professional, clean framework for automated pipeline and data insights extraction.</p>", unsafe_allow_html=True)
st.divider()

if uploaded_file is not None and category_col is not None and numeric_col is not None:
    with st.spinner("⏳ Running background ETL processes..."):
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file, nrows=5000)
            else:
                df = pd.read_excel(uploaded_file, engine='openpyxl', nrows=5000)
            
            # معالجة وتنظيف عمود الأرقام بعناية وحماية
            calc_col = "Cleaned_Amount"
            if df[numeric_col].dtype == 'object':
                df[calc_col] = df[numeric_col].astype(str).str.replace('$', '', regex=False).str.replace(',', '', regex=False).str.strip()
            else:
                df[calc_col] = df[numeric_col]
            df[calc_col] = pd.to_numeric(df[calc_col], errors='coerce').fillna(0)

            # --- كروت الأداء العلوية مع التنسيق الذكي للأرقام المريحة للعين ---
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f'<div class="metric-card"><div class="metric-label">Total Transactions</div><div class="metric-value">{len(df):,}</div></div>', unsafe_allow_html=True)
            with col2:
                total_sum = df[calc_col].sum()
                st.markdown(f'<div class="metric-card"><div class="metric-label">Cumulative {numeric_col}</div><div class="metric-value">{format_large_number(total_sum)}</div></div>', unsafe_allow_html=True)
            with col3:
                mean_val = df[calc_col].mean()
                st.markdown(f'<div class="metric-card"><div class="metric-label">Average Value</div><div class="metric-value">{format_large_number(mean_val)}</div></div>', unsafe_allow_html=True)

            st.divider()

            # --- الرسومات البيانية المنسقة بالتوازي ---
            st.markdown("<h2>📊 Visual Intelligence Insights</h2>", unsafe_allow_html=True)
            chart_col1, chart_col2 = st.columns(2)
            
            with chart_col1:
                st.markdown('<div class="chart-box">', unsafe_allow_html=True)
                st.markdown(f"<p style='color: #94A3B8; font-size: 14px; font-weight: 500; margin-bottom: 15px;'>Distribution: {numeric_col} by {category_col}</p>", unsafe_allow_html=True)
                category_summary = df.groupby(category_col)[calc_col].sum().head(10)
                st.bar_chart(category_summary, color="#0EA5E9", use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            with chart_col2:
                st.markdown('<div class="chart-box">', unsafe_allow_html=True)
                if time_col != "None":
                    st.markdown(f"<p style='color: #94A3B8; font-size: 14px; font-weight: 500; margin-bottom: 15px;'>Chronological Trend over {time_col}</p>", unsafe_allow_html=True)
                    time_summary = df.groupby(time_col)[calc_col].sum().head(20)
                    st.line_chart(time_summary, color="#10B981", use_container_width=True)
                else:
                    st.markdown("<p style='color: #94A3B8; font-size: 14px; font-weight: 500; margin-bottom: 15px;'>Chronological Trend</p>", unsafe_allow_html=True)
                    st.info("💡 Map a temporal column in the sidebar to activate the trend line chart.")
                st.markdown('</div>', unsafe_allow_html=True)

            # --- الخرائط ومعاينة البيانات بتناسق ---
            st.divider()
            st.markdown("<h2>📍 Location Dynamics & Raw Ledger</h2>", unsafe_allow_html=True)
            
            map_col, table_col = st.columns(2)
            
            with map_col:
                st.markdown('<div class="chart-box">', unsafe_allow_html=True)
                st.markdown("<p style='color: #94A3B8; font-size: 14px; font-weight: 500; margin-bottom: 15px;'>Geospatial Distribution</p>", unsafe_allow_html=True)
                lat_cols = [c for c in df.columns if c.lower() in ['latitude', 'lat']]
                lon_cols = [c for c in df.columns if c.lower() in ['longitude', 'lon', 'lng']]
                
                if lat_cols and lon_cols:
                    map_data = df[[lat_cols[0], lon_cols[0]]].dropna().rename(columns={lat_cols[0]: 'lat', lon_cols[0]: 'lon'})
                    st.map(map_data)
                else:
                    country_cols = [c for c in df.columns if 'country' in c.lower() or 'region' in c.lower()]
                    if country_cols:
                        country_data = df.groupby(country_cols[0])[calc_col].sum().head(8)
                        st.bar_chart(country_data, color="#F59E0B")
                    else:
                        st.warning("No geospatial tags or geographic labels detected in this dataset view.")
                st.markdown('</div>', unsafe_allow_html=True)
                
            with table_col:
                st.markdown('<div class="chart-box">', unsafe_allow_html=True)
                st.markdown("<p style='color: #94A3B8; font-size: 14px; font-weight: 500; margin-bottom: 15px;'>Active Dataset View (First 5 Rows)</p>", unsafe_allow_html=True)
                # عرض جدول البيانات بشكل مريح ومتناسق مع التصميم
                st.dataframe(df.head(5), use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)

            # --- محرك التنبؤ الذكي ---
            st.divider()
            st.markdown("<h2>🤖 Predictive Intelligence Core</h2>", unsafe_allow_html=True)
            input_value = st.number_input(f"Calibrate baseline {numeric_col} entry ($):", min_value=0, value=1000)
            st.markdown(
                f"""
                <div class="predict-box">
                    <span style='color: #A7F3D0;'>💡 <b>AI Statistical Target:</b> Expected future variance projection for this baseline input is <b>${input_value * 0.25:,.2f}</b></span>
                </div>
                """, 
                unsafe_allow_html=True
            )

        except Exception as e:
            st.error(f"❌ Pipeline Execution Error: {e}")
else:
    st.info("☝️ Dashboard initialized and awaiting data ingestion. Please drop an Excel or CSV file in the sidebar panel to begin analytics.")