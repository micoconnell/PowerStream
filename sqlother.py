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
listofOther = ['AFG1','BON1','CCMH','DAI1','GOC1','GPEC','NRG3','SLP1','SRL1','WWD1','WST1','WEY1','EAGL']
for x in range(len(listofOther)):
    stringGas = listofOther[x]
    cursor = init_connection()
    cursor.execute('''
                    UPDATE otherAB
                    SET {0} = 0
                    WHERE DateNum >= 20221005'''.format(stringGas))
    cursor.commit()



