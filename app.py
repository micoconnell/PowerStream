#streamlit run project_contents/app/app.py

import streamlit as st
import pyodbc
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import calendar
st.set_page_config(page_title="Dahlia", page_icon="random", layout="wide", initial_sidebar_state="expanded")
st.title("Dahlia")

tabs = st.tabs(["Open Interest By Month Through Time", "Plots", "reports"])

tab_metrics = tabs[0]
#@st.experimental_singleton
#@st.cache(suppress_st_warning=True) 
def init_connection():
    
    server =r'tcp:supowerdatabase.database.windows.net' 
    database =r'SUpowerFinancials' 
    username =r'micoconnell1' 
    password =r'anisoTropical+308'
    driver= r'{ODBC Driver 17 for SQL Server}'
    
    cnxn = pyodbc.connect('DRIVER=' + driver + ';SERVER=' +
    server + ';PORT=1433;DATABASE=' + database +
    ';UID=' + username + ';PWD=' + password)
    cursor = cnxn.cursor()
    return cursor

cursor = init_connection()
top_var = 100
result = cursor.execute('SELECT * FROM dbo.AzureBlobStorageFile ORDER BY dateModified DESC')
rows = result.fetchall()
cols = []
for i,_ in enumerate(result.description):
    cols.append(result.description[i][0])

df = pd.DataFrame(np.array(rows), columns=cols)
#@st.cache(suppress_st_warning=True) 
with tab_metrics:
    col1,col2,col3=st.columns(3)
    
    cursor = init_connection()
    result = cursor.execute('SELECT * FROM dbo.AzureBlobStorageFile ORDER BY dateModified DESC')
    rows = result.fetchall()
    cols = []
    for i,_ in enumerate(result.description):
        cols.append(result.description[i][0])

    df = pd.DataFrame(np.array(rows), columns=cols)
    year = st.selectbox('Year', range(2020, 2050))
    month = st.selectbox('Month', range(1, 13))


    
    d = datetime.datetime(year, month, 1)
    date = pd.to_datetime(d)
    dateY = date.strftime('%Y')
    date = date.strftime('%Y-%m-%d')
    
    currentMonthName = calendar.month_name[d.month]
    




    df['BeginDate'] = pd.Series(df['BeginDate'], dtype="string")
    df['EndDate'] = pd.Series(df['EndDate'], dtype="string")
    df['DateModified'] = pd.Series(df['DateModified'], dtype="string")
    df['Settle'] = pd.Series(df['Settle'], dtype="string")
    df['netOI'] = pd.Series(df['netOI'], dtype="string")



    df['netOI'] = df['netOI'].apply(pd.to_numeric)
    #df['Settle'] = df['netOI'].apply(pd.to_numeric)


    df = df[(df['BeginDate'] == date)]
    df["BeginDate"] = pd.to_datetime(df["BeginDate"], format="%Y/%m/%d")
    df["EndDate"] = pd.to_datetime(df["EndDate"], format="%Y/%m/%d")

    df["DAYSDIFF"] = (df["EndDate"] - df["BeginDate"]) / np.timedelta64(1, 'h') + 24
    df = df[(df['DAYSDIFF'] > 24)]
    df['netOI'] = df['netOI'] / df['DAYSDIFF']
    df = df.drop(['DAYSDIFF'],axis=1)
    df['BeginDate'] = pd.Series(df['BeginDate'], dtype="string")
    df['EndDate'] = pd.Series(df['EndDate'], dtype="string")
    df['DateModified'] = pd.Series(df['DateModified'], dtype="string")
    df['Settle'] = pd.Series(df['Settle'], dtype="int")
    df['netOI'] = pd.Series(df['netOI'], dtype="int")
    df['netOI'] = df['netOI'].apply(pd.to_numeric)
    df['Settle'] = df['Settle'].apply(pd.to_numeric)
    df['netOI'] = df['netOI'].round(decimals = 0)
    
    df.drop_duplicates(inplace=True,subset=['DateModified'])
    df.set_index(df['DateModified'],inplace=True)
    


    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add traces
    fig.add_trace(
        go.Bar(x=df.index, y=df.netOI, name="Open Interest (MW)"),
        secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(x=df.index, y=df.Settle, name="Price ($/MW)"),
        secondary_y=True,
    )
    fig.update_layout(yaxis_range=[0,2000])
    fig.update_layout(yaxis2_range=[0,1000])
    fig.update_yaxes(title_text="<b>Net Open Interest</b>", secondary_y=False)
    fig.update_yaxes(title_text="<b>Price (MW)</b>", secondary_y=True)
    fig.update_xaxes(title_text="Open Interest For" + " " + currentMonthName + " " + str(year))
    fig.update_layout(
    autosize=False,
    width=900,
    height=400,
    
    )

    st.columns(spec =1)
    col1, col2 = st.columns([1, 1])


    col1.subheader("Open Interest Details")
    

    col2.subheader("Open Interest Vs Settle (Through Time)")
    col1.write(df)
    col2.plotly_chart(fig)

    
    st.dataframe(data=df,height=300,width=1000)

        
    st.plotly_chart(fig)
    

