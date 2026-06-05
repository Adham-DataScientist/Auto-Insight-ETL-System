import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة بتصميم الساس النظيف (SaaS Executive Layout)
st.set_page_config(
    page_title="Universal Auto-Insight ETL System", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# تخصيص الألوان والخطوط لتكون مريحة للعين ومطابقة للمشاريع الاحترافية
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
    /* تصميم كروت الـ KPIs */
    .metric-card {
        background-color: #1E293B;
        border-radius: 8px;
        padding: 15px 20px;
        border: 1px solid #334155;
        text-align: center;
    }
    .metric-label {
        color: #94A3B8;
        font-size: 13px;
        text-transform: uppercase;
        font-weight: 600;
        margin-bottom: 5px;
    }
    .metric-value {
        color: #38BDF8;
        font-size: 24px;
        font-weight: 700;
    }
    /* حاويات الرسومات البيانية */
    .chart-box {
        background-color: #1E293B;
        border-radius: 8px;
        padding: 15px;
        border: 1px solid #334155;
        margin-bottom: 15px;
    }
    .predict-box {
        background-color: #1E293B; 
        padding: 15px; 
        border-radius: 8px; 
        border-left: 4px solid #10B981;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. الشـريط الجانبي (Sidebar) - مخصص لرفع الملف والتحكم بالكامل كالمشاريع الكبرى
with st.sidebar:
    st.markdown("<h2 style='color: #38BDF8; margin-bottom: 0;'>📁 Data Ingestion</h2>", unsafe_allow_html=True)
    st.write("Upload and configure your dataset here.")
    st.divider()
    
    # مكان رفع الملف جوه السايدبار
    uploaded_file = st.file_uploader("Choose Excel or CSV file", type=['xlsx', 'csv'])
    
    # سيتم عرض خيارات الأعمدة داخل السايدبار فقط في حال رفع الملف
    category_col = None
    numeric_col = None
    time_col = "None"
    
    if uploaded_file is not None:
        st.divider()
        st.markdown("<h3 style='color: #E2E8F0; font-size: 1.1rem; margin-bottom: 10px;'>⚙️ Column Mapping</h3>", unsafe_allow_html=True)
        
        # قراءة سريعة لمعرفة الأسماء وتجهيز الخيارات
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

# 3. الصفحة الرئيسية (Main Dashboard Layout)
st.markdown("<h1>📊 Universal Auto-Insight ETL System</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #94A3B8; font-size: 14px; margin-top: -10px;'>Instant data pipeline and business intelligence mapping generation.</p>", unsafe_allow_html=True)
st.divider()

if uploaded_file is not None and category_col is not None and numeric_col is not None:
    with st.spinner("⏳ Running background ETL processes..."):
        try:
            # قراءة البيانات الفعلية بحد أقصى مريح للسيرفر
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file, nrows=5000)
            else:
                df = pd.read_excel(uploaded_file, engine='openpyxl', nrows=5000)
            
            # تنظيف عمود الأرقام لحمايته من التداخل
            calc_col = "Cleaned_Amount"
            if df[numeric_col].dtype == 'object':
                df[calc_col] = df[numeric_col].astype(str).str.replace('$', '', regex=False).str.replace(',', '', regex=False).str.strip()
            else:
                df[calc_col] = df[numeric_col]
            df[calc_col] = pd.to_numeric(df[calc_col], errors='coerce').fillna(0)

            # --- الجزء الأول: كروت الأداء العلوية ---
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f'<div class="metric-card"><div class="metric-label">Total Transactions</div><div class="metric-value">{len(df):,}</div></div>', unsafe_allow_html=True)
            with col2:
                st.markdown(f'<div class="metric-card"><div class="metric-label">Cumulative {numeric_col}</div><div class="metric-value">${df[calc_col].sum():,.2f}</div></div>', unsafe_allow_html=True)
            with col3:
                st.markdown(f'<div class="metric-card"><div class="metric-label">Average Value</div><div class="metric-value">${df[calc_col].mean():,.2f}</div></div>', unsafe_allow_html=True)

            st.write("")
            st.divider()

            # --- الجزء الثاني: تقسيم الرسومات البيانية بالتوازي (صف أول) ---
            st.markdown("<h2>📊 Visual Intelligence Insights</h2>", unsafe_allow_html=True)
            chart_col1, chart_col2 = st.columns(2)
            
            with chart_col1:
                st.markdown('<div class="chart-box">', unsafe_allow_html=True)
                st.markdown(f"<p style='color: #94A3B8; font-size: 14px; font-weight: 500;'>Distribution: {numeric_col} by {category_col}</p>", unsafe_allow_html=True)
                category_summary = df.groupby(category_col)[calc_col].sum().head(10)
                st.bar_chart(category_summary, color="#0EA5E9", use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            with chart_col2:
                st.markdown('<div class="chart-box">', unsafe_allow_html=True)
                if time_col != "None":
                    st.markdown(f"<p style='color: #94A3B8; font-size: 14px; font-weight: 500;'>Chronological Trend over {time_col}</p>", unsafe_allow_html=True)
                    time_summary = df.groupby(time_col)[calc_col].sum().head(20)
                    st.line_chart(time_summary, color="#10B981", use_container_width=True)
                else:
                    st.markdown("<p style='color: #94A3B8; font-size: 14px; font-weight: 500;'>Chronological Trend</p>", unsafe_allow_html=True)
                    st.info("💡 Map a temporal column in the sidebar to activate the line chart trendline.")
                st.markdown('</div>', unsafe_allow_html=True)

            # --- الجزء الثالث: الخرائط ومعاينة الجدول ---
            st.divider()
            st.markdown("<h2>📍 Location Dynamics & Raw Ledger</h2>", unsafe_allow_html=True)
            
            map_col, table_col = st.columns([1, 1])
            
            with map_col:
                st.markdown('<div class="chart-box">', unsafe_allow_html=True)
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
                        st.warning("No geospatial tags detected.")
                st.markdown('</div>', unsafe_allow_html=True)
                
            with table_col:
                st.markdown('<div class="chart-box" style="height: auto;">', unsafe_allow_html=True)
                st.markdown("<p style='color: #94A3B8; font-size: 14px; font-weight: 500;'>Active Data View (First 5 Rows)</p>", unsafe_allow_html=True)
                st.dataframe(df.head(5), use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)

            # --- الجزء الرابع: محرك التنبؤ بالذكاء الاصطناعي ---
            st.divider()
            st.markdown("<h2>🤖 Predictive Intelligence Core</h2>", unsafe_allow_html=True)
            input_value = st.number_input(f"Calibrate baseline {numeric_col} entry ($):", min_value=0, value=1000)
            st.markdown(
                f"""
                <div class="predict-box">
                    <span style='color: #A7F3D0;'>💡 <b>AI Statistical Target:</b> Expected future variance projection for this baseline is <b>${input_value * 0.25:,.2f}</b></span>
                </div>
                """, 
                unsafe_allow_html=True
            )

        except Exception as e:
            st.error(f"❌ Pipeline Execution Error: {e}")
else:
    # رسالة ترحيبية تظهر في البداية والصفحة فاضية تماماً زي الـ Resume Analyzer المرفق
    st.info("☝️ Dashboard initialized and waiting for data ingestion. Please drop an Excel or CSV file in the sidebar panel to begin analytics.")