import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة والتصميم الداكن
st.set_page_config(page_title="Universal Auto-Insight Dashboard", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; }
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

# 2. رفع الملف
uploaded_file = st.file_uploader("Upload your Sales Data File", type=['xlsx', 'csv'])

if uploaded_file is not None:
    with st.spinner("⏳ Analyzing data... Please wait..."):
        try:
            # قراءة الملف بطريقة موفرة للذاكرة
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file, nrows=20000)
            else:
                df = pd.read_excel(uploaded_file, engine='openpyxl', nrows=5000)
                
            st.success(f"✅ Successfully loaded '{uploaded_file.name}' with {df.shape[0]} rows!")
            st.divider()

            # عرض أول 5 أسطر من البيانات
            st.subheader("📑 Data Preview")
            st.dataframe(df.head(5), use_container_width=True)
            
            st.divider()

            # ---- [إعدادات الفلترة الديناميكية] ----
            st.subheader("⚙️ Configure Your Dashboard Columns")
            all_columns = df.columns.tolist()
            
            col_setup1, col_setup2, col_setup3 = st.columns(3)
            with col_setup1:
                category_col = st.selectbox("Select Categorical Column (e.g., day_name):", all_columns, index=0)
            with col_setup2:
                # محاولة اختيار عمود مختلف تلقائياً لتفادي لغبطة المستخدم
                default_num_index = 1 if len(all_columns) > 1 else 0
                numeric_col = st.selectbox("Select Numeric Column:", all_columns, index=default_num_index)
            with col_setup3:
                time_col = st.selectbox("Select Time/Date Column (Optional):", ["None"] + all_columns)

            st.divider()

            # ---- [فحص وحماية الحسابات من التضارب] ----
            # بنعمل عمود جديد خالص مخصص للحسابات عشان الأعمدة الأصلية متضربش
            calc_col = "Cleaned_Amount"
            
            if df[numeric_col].dtype == 'object':
                df[calc_col] = df[numeric_col].astype(str).str.replace('$', '', regex=False).str.replace(',', '', regex=False).str.strip()
            else:
                df[calc_col] = df[numeric_col]
                
            df[calc_col] = pd.to_numeric(df[calc_col], errors='coerce').fillna(0)

            # ---- [عرض مؤشرات الأداء الحية KPIs] ----
            st.subheader("📈 Dynamic Business Insights")
            
            metric1, metric2, metric3 = st.columns(3)
            metric1.metric("Processed Transactions", f"{len(df):,}")
            metric2.metric(f"Total {numeric_col}", f"${df[calc_col].sum():,.2f}")
            metric3.metric(f"Average {numeric_col}", f"${df[calc_col].mean():,.2f}")

            # ---- [الرسومات البيانية التفاعلية] ----
            chart_col1, chart_col2 = st.columns(2)
            
            with chart_col1:
                st.write(f"**Total {numeric_col} by {category_col}**")
                # التجميع بيحصل بآمان هنا لأن الحسابات في عمود منفصل
                category_summary = df.groupby(category_col)[calc_col].sum().head(15)
                st.bar_chart(category_summary)
            
            with chart_col2:
                if time_col != "None":
                    st.write(f"**{numeric_col} Trends Over {time_col}**")
                    time_summary = df.groupby(time_col)[calc_col].sum().head(30)
                    st.line_chart(time_summary)
                else:
                    st.warning("⚠️ Select a Time Column to display the trend line chart.")

            # ---- [محرك التنبؤ المبسط] ----
            st.divider()
            st.subheader("🤖 AI Profit Predictor")
            input_value = st.number_input(f"Enter baseline {numeric_col} value ($):", min_value=0, value=1000)
            st.info(f"💡 Estimated future profit target: **${input_value * 0.25:,.2f}**")

        except Exception as e:
            st.error(f"❌ Error processing file: {e}")
else:
    st.info("☝️ Please upload an Excel or CSV file to start the automated analysis.")