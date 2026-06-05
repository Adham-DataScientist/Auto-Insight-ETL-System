import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from functions import proccess_date 

# 1. إعدادات الصفحة والتصميم
st.set_page_config(page_title="Auto-Insight ETL Dashboard", layout="wide")

st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    [data-testid="stMetric"] {
        background-color: #1e2130;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #2d3142;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. العناوين الرئيسية
st.title("📊 Auto-Insight ETL System")
st.markdown("Welcome, My Dear ❤️")

# 3. رفع الملف
uploaded_file = st.file_uploader("Cleaned_Shipping_Data", type=['xlsx'])

if uploaded_file is not None:
    # قراءة الداتا وتجهيزها بمجرد رفع الملف عشان نضمن ثبات العرض
    df = pd.read_excel(uploaded_file)
    df = proccess_date(df)
    
    st.success("✅ Data loaded and processed successfully!")
    st.divider()

    # ---- [الجزء الأول: عرض البيانات والمؤشرات] ----
    st.subheader("📑 Processed Data Preview")
    st.dataframe(df.head(), use_container_width=True) 
    
    st.write("") # مسافة تجميلية
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Rows", f"{len(df):,}")
    col2.metric("Total Profits", f"${df['Profits'].sum():,.2f}")
    col3.metric("Avg Price", f"${df['Price'].mean():,.2f}")

    st.divider()

    # ---- [الجزء الثاني: التحليلات والرسومات البيانية] ----
    st.subheader("📊 Visual Insights")
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        st.write("**Profits by Country**")
        st.bar_chart(df.groupby('Country')['Profits'].sum())
    
    with chart_col2:
        # ترتيب الشهور بشكل صحيح
        months_order = ['January', 'February', 'March', 'April', 'May', 'June', 
                        'July', 'August', 'September', 'October', 'November', 'December']
        df['Month'] = pd.Categorical(df['Month'], categories=months_order, ordered=True)
        
        st.write("**Profit Trends Across Months**")
        st.line_chart(df.groupby('Month', observed=False)['Profits'].sum())
    
    st.divider() 

    # ---- [الجزء الثالث: التنبؤ بالذكاء الاصطناعي] ----
    st.subheader("🤖 AI Profit Predictor")
    price_input = st.number_input("Enter Price to predict profit ($):", min_value=0, value=1000, step=50)
    
    # حساب التنبؤ (معادلة خطية مبسطة)
    predicted_profit = price_input * 0.25 
    
    st.info(f"💡 Estimated Profit for **${price_input:,}**: **${predicted_profit:,.2f}**")

else:
    st.info("☝️ يرجى اختيار ملف الإكسيل أولاً للبدء في تحليل البيانات (Browse files)")