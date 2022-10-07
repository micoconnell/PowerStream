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
listofGas = ['ANC1','ALP1','BHL1','GEN5','ENC1','ENC2','ENC3','CRS1','CRS2','CRS3','DRW1','HRM','GEN6','MEO3','MEO4','MEO2','NPC2','NPC3','NPP1','ALP2','PH1','RB5','NAT1','SET1','VVW1','VVW2','WCD','PMB1','ALS1','HMT1','SCR1','BCRK','BCR2','BFD1','CNR5','COD1','CRG1','SHCG','TC01','CL01','DOWG','TLM2','EPS1','SCR6','FH1','ECO4','HRT4','JOF1','IOR3','PEC1','MEG1','MKRC','IOR1','MUL1','MKR1','IOR2','NXO2','SCR5','PR1','RL1','TCO2','SDH1','APS1','IOR4','SCL1','UOC1','UOA1','ECO1','CAL1','FNG1','CMH1','NX01','EGC1','BR4','BR5','KH2','KH3','SH1','SH2','SD6']

for x in range(len(listofGas)):
    stringGas = listofGas[x]
    cursor = init_connection()
    cursor.execute('''
                    UPDATE gasAb
                    SET {0} = 0
                    WHERE DateNum >= 20221005'''.format(stringGas))
    cursor.commit()



