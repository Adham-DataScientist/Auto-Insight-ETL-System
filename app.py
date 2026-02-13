import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from functions import proccess_date 

st.set_page_config(page_title="Auto-Insight ETL Dashboard", layout="wide")
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    stMetric {
        background-color: #1e2130;
        padding: 15px;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)


st.title("📊 Adham_Auto-Insight ETL System")
st.markdown("اهلا ومرحبا بكم في موقع ادهم ابو عوض \n \n لتحليل البيانات ")

uploaded_file = st.file_uploader("Updatee_Sales_Analysis_Report", type=['xlsx'])

if uploaded_file is not None :
    
    if st.button("🚀 Start Data Analysis"):
        df = pd.read_excel(uploaded_file)
    
        df = proccess_date(df)
    
        st.subheader("📑 Processed Data Preview")
        st.dataframe(df.head()) 
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Rows", len(df))
        col2.metric("Total Profits", f"${df['Profits'].sum():,.2f}")
        col3.metric("Avg Price", f"${df['Price'].mean():,.2f}")

    

        st.subheader("📈 Business Insights")
        fig, ax = plt.subplots()
        df.groupby('Country')['Profits'].sum().plot(kind='bar', ax=ax)
        st.pyplot(fig)
    
    
        st.divider() 
    
        st.subheader("🤖 AI Profit Predictor")
        price_input = st.number_input("Enter Price to predict profit:", min_value=0, value=1000)
    

        test_data = pd.DataFrame([[price_input]], columns=['Price'])

        predicted_profit = price_input * 0.25 
    
        st.write(f"Estimated Profit for ${price_input}: **${predicted_profit:,.2f}**")


        st.subheader("📊 Visual Insights")
        chart_col1, chart_col2 = st.columns(2)
    
        with chart_col1:
           st.write("Profits by Country")
           st.bar_chart(df.groupby('Country')['Profits'].sum())
        
        with chart_col2:
       
            months_order = ['January', 'February', 'March', 'April', 'May', 'June', 
                'July', 'August', 'September', 'October', 'November', 'December']
            df['Month'] = pd.Categorical(df['Month'], categories=months_order, ordered=True)

       
            st.line_chart(df.groupby('Month')['Profits'].sum())
            st.write("Sales Type Distribution")
            st.line_chart(df.groupby('Month')['Profits'].sum())
else:
    st.info("☝️ (Browse files)  يرجي اختيار الملف من")    
    