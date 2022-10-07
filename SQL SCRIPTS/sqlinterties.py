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
listofIntertie =   ['BCMATLIM' ,'BCIM','MATLIM','SASKIM']

for x in range(len(listofIntertie)):
    stringGas = listofIntertie[x]
    cursor = init_connection()
    cursor.execute('''
                    UPDATE intertieAB
                    SET {0} = 0
                    WHERE DateNum >= 20221005'''.format(stringGas))
    cursor.commit()


