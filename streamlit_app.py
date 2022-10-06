#streamlit run project_contents/app/app.py
from datetime import timedelta
import streamlit as st
import pyodbc
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import calendar
from datetime import date 

st.set_page_config(page_title="Dahlia", page_icon="random", layout="wide", initial_sidebar_state="expanded")
st.title("Dahlia")

tabs = st.tabs(["Open Interest By Month Through Time", "Plots", "reports"])

tab_metrics = tabs[0]
tab_flags = tabs[1]

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
#@st.cache(suppress_st_warning=True) 
with tab_flags:
    
    datetime_object = datetime.date(2022, 9, 21)
    currentTimeDate = date.today() + timedelta(14)
    currentTime = currentTimeDate.strftime('%Y-%m-%d')
    dateOfInterest = st.date_input(label ='Date', value=None, min_value=datetime_object, max_value=currentTimeDate, key=None, help=None, on_change=None, args=None, kwargs=None)
    col1,col2=st.columns(2)
    hourzerotab = 0
    endhourzerotab=23
    print(dateOfInterest.year)
    daystartSQL = datetime.datetime(dateOfInterest.year,dateOfInterest.month,dateOfInterest.day)
    daystart = datetime.datetime(dateOfInterest.year,dateOfInterest.month,dateOfInterest.day,hourzerotab)
    daylast = datetime.datetime(dateOfInterest.year,dateOfInterest.month,dateOfInterest.day,endhourzerotab)
    d = datetime.datetime(dateOfInterest.year, dateOfInterest.month, dateOfInterest.day)
    dateLast = pd.to_datetime(daylast)
    dateStart = pd.to_datetime(daystart)
    currentMonthName = calendar.month_name[d.month]
    cursor = init_connection()
    result = cursor.execute("SELECT * FROM dbo.AILForecasts WHERE begin_datetime_mpt >= ?", daystart)
    rows = result.fetchall()
    cols = []
    for i,_ in enumerate(result.description):
        cols.append(result.description[i][0])

    df = pd.DataFrame(np.array(rows), columns=cols)

    df = df.drop(['begin_datetime_utc'],axis=1)

    df['begin_datetime_mpt'] = pd.Series(df['begin_datetime_mpt'], dtype="string")
    df['dateModified'] = pd.Series(df['dateModified'], dtype="string")
    df['alberta_internal_load'] = pd.Series(df['alberta_internal_load'], dtype="string")
    df['alberta_internal_load'] = df['alberta_internal_load'].apply(pd.to_numeric)
    df['forecast_alberta_internal_load'] = pd.Series(df['forecast_alberta_internal_load'], dtype="string")
    df['forecast_alberta_internal_load'] = df['forecast_alberta_internal_load'].apply(pd.to_numeric)
    df["begin_datetime_mpt"] = pd.to_datetime(df["begin_datetime_mpt"], format="%Y/%m/%d %H")
    df["dateModified"] = pd.to_datetime(df["dateModified"])
    dl = df
    dl =dl[dl['begin_datetime_mpt'] >= dateStart]
    dl =dl[dl['begin_datetime_mpt'] <= dateLast]
    dl.set_index(['begin_datetime_mpt', 'dateModified'])
    dl.sort_values(by=[('begin_datetime_mpt'),('dateModified')])
    listunique = []
    listunique = dl['dateModified'].unique()
    
    firstDate = listunique[-1]
    firstDate = pd.to_datetime(firstDate)

    lastDate = listunique[0]
    lastDate = pd.to_datetime(lastDate)
    #st.dataframe(dab)



    #index = listunique.index(start_time)
    ## Need some way of figuring out how to make the scroll bar tied into the listunique. 
    dab = dl[dl['dateModified'] == listunique[1]]
    start_time = st.slider(
        "Start with Historical Lookup?",
        value=daystart,
        format="MM/DD/YY")
    st.write("Start time:", start_time)
    numpy_date = np.datetime64(start_time)
    res = [x for x in range(len(listunique)) if listunique[x] == numpy_date]
    print("AYE")
    print(res)
    #dab = dl[dl['dateModified'] == listunique[47]]
    print(dab)
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(x=dab.begin_datetime_mpt, y=dab.forecast_alberta_internal_load, name="hello",mode = 'lines',
                            line=dict(width=1)))
    col1.plotly_chart(fig)
    #st.plotly_chart(fig)
    fig1 = go.Figure()
    for num in range(1,len(listunique)):
        dab = dl[dl['dateModified'] == listunique[num]]
        fig1.add_trace(go.Scatter(x=dab.begin_datetime_mpt, y=dab.forecast_alberta_internal_load, name='High 2014',mode = 'lines',
                            line=dict(width=1)))
        
    #st.plotly_chart(fig1)
    col2.plotly_chart(fig1)
    








with tab_metrics:
    col1,col2=st.columns(2)
    df = pd.DataFrame(np.array(rows), columns=cols)
    year = st.selectbox('Year', range(2023, 2035))
    month = st.selectbox('Month', range(1, 13))


    
    d = datetime.datetime(year, month, 1)
    date = pd.to_datetime(d)
    dateY = date.strftime('%Y')
    date = date.strftime('%Y-%m-%d')
    cursor = init_connection()
    result = cursor.execute('SELECT * FROM dbo.AzureBlobStorageFile WHERE BeginDate = ? ORDER BY dateModified DESC', date)
    rows = result.fetchall()
    cols = []
    for i,_ in enumerate(result.description):
        cols.append(result.description[i][0])

    df = pd.DataFrame(np.array(rows), columns=cols)



    
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
    fig.update_layout(yaxis2_range=[0,500])
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



