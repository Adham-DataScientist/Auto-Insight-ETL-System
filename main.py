import pandas as pd 
import tkinter as tk 
import os 
from tkinter import filedialog
from functions import load_data , proccess_date , setup_enviroment , start_robot
import matplotlib.pyplot as plt 
from sklearn.linear_model import LinearRegression
from SqlServer import export_sql

def main ():
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost" , True)
    
    
    file_path=filedialog.askopenfilename(
        title="Select file",
        filetypes=[("Excel File" , "*.xlsx *.xls") , ("CSV File" , ".csv")]
    )
    
    if file_path :
        try :
            df =load_data(file_path)
            if df is not None :
                proccess_date(df)
                export_sql(df)
                
                df = df.drop(columns=['Date'])
            print(f"you have {df.shape[0]} rows and {df.shape[1]} columns")
            
            
            df['paid_by_years'] = df.groupby("Year")['Paid'].sum().plot(kind="bar",fontsize=14,title="paid_of_year",color=["red" ,"yellow"])
            plt.savefig("Chart/paid_of_year.png")
            plt.close()
            
            df['Profits_by_years'] = df.groupby("Year")['Profits'].sum().plot(kind="barh",title="Profits_of_year",fontsize=14, color=["green" ,"red"])
            plt.savefig("Chart/Profits_of_year.png")
            plt.close()
            
            df['Max_of_Paid'] = df["Paid"].max()
        
            df['profit_by_country'] = df.groupby("Country")["Profits"].max().plot(kind="barh",title="Max_profit",fontsize=12,color=['red' ,'green' ,'yellow','blue'])
            plt.savefig("Chart/profit_by_country.png")
            plt.close()
            
            df["country_of_Sales type"] = df.groupby("Country")["Paid"].sum().plot(kind="barh" , title="country_of_Paid",fontsize=12,color=['red' ,'yellow' ,'green','blue'])
            plt.savefig("Chart/country_of_Sales type.png")
            plt.close()
            
            df["Paid_of_Sales_type"] = df.groupby("Sales type")["Paid"].sum().plot(kind="pie" ,title="Paid_of_Sales type",fontsize=12,autopct="%1.1f%%", color=['red' ,'yellow'])
            plt.savefig("Chart/Paid_of_Sales_type.png")
            plt.close()
            
            df["Profits_by_Direction"] = df.groupby("Direction")["Profits"].sum().plot(kind="line" ,title="Profits_by_Direction",fontsize=12)
            plt.savefig("Chart/Profits_by_Direction.png")
            plt.close()
            
            
            outpot_file =os.path.join("Outpot" , "Final_Shipping_Data.xlsx")
            with pd.ExcelWriter(outpot_file) as writer :
                df.to_excel(writer , sheet_name="Clened Data" , index=False)
                summry=df.groupby("Country")['Profits'].agg(["sum","mean","max"])
                summry.to_excel(writer , sheet_name="excutive_summry")
                print(f"✅ Project completed! Report saved in: {outpot_file}")
            
            df.to_excel("Cleaned_Shipping_Data.xlsx" , index=False)    
            print(df.head())
            print(df.describe())
            print(df.info())
            save_csv=df.to_csv("Uploaded_CSV.csv"  , index=False)
            print( "Saved CSV" ,save_csv)
         
            
            
   
    
            
  
            
        except Exception as a :
            print(f"Error loading data {a}")    
    else :
        print("No selcted data")    
    
    x =df[['Price']]
    y =df['Profits']
            
    model_auto =LinearRegression()
    model_auto.fit(x , y)
            
    test = pd.DataFrame([[1000]] , columns=['Price'])
    predicted = model_auto.predict(test)
    print(f"The final exam \n {predicted[0]:.0f}")      
                
    
if __name__ =="__main__":
    main()  
setup_enviroment()    
start_robot()  
