import pandas as pd 
import os 
import matplotlib.pyplot as plt 
import tkinter as tk 
from tkinter import filedialog
import shutil
import time
from  sklearn.linear_model import LinearRegression

def load_data(file_path):
    try : 
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
            print('Download CSV')
        elif file_path.endswith('.xlsx') or file_path.endswith('.xls') :
            df =pd.read_excel(file_path)
            print("Download Excel")
        else :
            print("No Selected file") 
        return df
    except Exception as a :
        print(f"Error {a} already exists")   
        
def proccess_date (df):
    if 'Date' in df.columns :
        df['Date'] = pd.to_datetime(df['Date'])
        df['Year'] = df['Date'].dt.year                
        df['Month'] = df['Date'].dt.month_name               
        df['Day'] = df['Date'].dt.day_name                
        return df
        
def setup_enviroment():
    folders =['Input','Outpot','archive']
    
    for file in folders :
        try :
            if not os.path.exists(file):
                os.makedirs(file)
                print("New Create Files")
        except Exception as a :
            print(f"already file exists {a}")     
            
def start_robot():
    while True :
        input_dir ="Input"
        archive_dir ="archive"
        
        path =os.listdir(input_dir)
        
        if len(path) > 0:
            print(f"New Proccess File {path} ")
            
            for file in path :
                current_path = os.path.join(input_dir ,file )
                
                try : 
                    if file.endswith('.csv'):
                        df=pd.read_csv(current_path)
                        print("Download CSV")
                    elif file.endswith('.xlsx') or file.endswith(".xls"):
                        df=pd.read_excel(current_path)
                        print("Download Excel")   
                    else :
                        print("No Selected file")
                        continue    
                    
                    if not os.path.exists(archive_dir):
                        os.makedirs(archive_dir)
                        
                    distination = os.path.join(archive_dir , file)     
                    shutil.move(current_path , distination)
                    print("Move is file to archive successfuly")
                except Exception as a :
                    print (f"Error is file {a}")    
            break
        else :
            print("NoT found New files ")
            time.sleep(10)      

    
    
                  
                                       
                