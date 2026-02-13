import urllib.parse
from   sqlalchemy import  create_engine
def export_sql (df):
    server_name =r".\SQLEXPRESS"
    database_name = "Auto_Insight"
    table_name = "auto_insight"
    
    Connection_String = (
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={server_name};"
        f"DATABASE={database_name};"
        f"Trusted_Connection=yes;"
        
    )
    quoted_conn = urllib.parse.quote_plus(Connection_String)
    engine = create_engine(f"mssql+pyodbc:///?odbc_connect={quoted_conn}"  ,fast_executemany = True)
    df.to_sql(table_name , con=engine , if_exists ="replace" , index = False , chunksize = 2000)
    