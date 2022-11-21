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
min_date = datetime.date(2022,1,1)
max_date = datetime.date(2050,1,1)
base = datetime.date(2022,1,1)
dates = [base + datetime.timedelta(days=x) for x in range(8000)]
ss = st.session_state
ss.analysis = {"filter": {}}

def updateDateRange():
    if 'dateRange' in ss and isinstance(ss.dateRange, tuple) and len(ss.dateRange)==2:
        st.write("##############")    # <-- with this it works, as it is supposed to be....but why?
        ss["analysis"]["filter"]['dateRange'] = (ss.dateRange[0].strftime("%Y%m%d"), ss.dateRange[1].strftime("%Y%m%d"))

if "dateRange" not in ss:
    ss.defaultDateRange = (dates[0], dates[-1])

st.date_input(
    label="Select date range",
    value=ss.defaultDateRange,
    min_value=min_date,
    max_value=max_date,
    key="dateRange",
    on_change=updateDateRange,
)

if isinstance(ss.dateRange, tuple) and len(ss.dateRange)==2 and "dateRange" not in ss["analysis"]["filter"]:
    ss["analysis"]["filter"]["dateRange"] = (ss.dateRange[0].strftime("%Y%m%d"), ss.dateRange[1].strftime("%Y%m%d"))


@st.cache(allow_output_mutation=True)
def button_states():
    return {"pressed": None}



first_ok = button_states()
ok_Coal = button_states()
ok_Gas = button_states()
ok_Hydro = button_states()
ok_Intertie = button_states()
ok_Energy = button_states()
ok_DualFuel = button_states()
ok_Other = button_states()
ok_Solar = button_states()
ok_Wind = button_states()
button_ok = st.button("Correct")
button_ok = first_ok
user_input = st.text_input("MegaWatt Impact:", 0)

if button_ok:
    first_ok.update({"pressed": True})
    if button_ok:
        first_ok.update({"pressed": not first_ok["pressed"]})
    
    
    option = st.selectbox(
            'Select Asset Type',
            ('Coal', 'Gas','Hydro','Intertie','Energy','Other','Dual Fuel','Solar','Wind'))
    st.write('You selected:', option, ". These are the current", option,"plants in the database:")
    if option == 'Coal':
        ok_Coal.update({"pressed": True})
    if option == 'Gas':
        ok_Gas.update({"pressed": True})
    if option == 'Hydro':
        ok_Hydro.update({"pressed": True})
    if option == 'Intertie':
        ok_Intertie.update({"pressed": True})
    if option == 'Other':
        ok_Other.update({"pressed": True})
    if option == 'Dual Fuel':
        ok_DualFuel.update({"pressed": True})
    if option == 'Energy':
        ok_Energy.update({"pressed": True})
    if option == 'Solar':
        ok_Solar.update({"pressed": True})
    if option == 'Wind':
        ok_Wind.update({"pressed": True})



    if option =='Coal':
        ques = st.radio("Pick available Coal plants:",('GN1','GN2','GN3','Unknown'),horizontal = True)
        name = ques
        st.write('You have selected',name,'. Please confirm that the dates: ', ss.dateRange[0], 'to ', ss.dateRange[1], 'are correct. If these dates are not correct, please press the reset button now. ' )
        button_Submit = st.button("Submit")
        startDate = ss.dateRange[0].strftime("%Y%m%d")
        endDate = ss.dateRange[-1].strftime("%Y%m%d")
        if button_Submit:
            button_finalChanges = st.button("Pressing this box will make these changes to the database. Are you Sure?")
            if button_finalChanges:
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
                cursor.execute('''
                            UPDATE coalAB
                            SET {0} = 0
                            WHERE DateNum >= ? AND DateNum <= ?'''.format(name),startDate,endDate)
                cursor.commit()



    if option =='Gas':


        ques = st.radio("Pick available Coal plants:",('ANC1','ALP1','BHL1','GEN5','ENC1','ENC2','ENC3','CRS1','CRS2','CRS3','DRW1','HRM','GEN6','MEO3','MEO4',
        'MEO2','NPC2','NPC3','NPP1','ALP2','PH1','RB5','NAT1','SET1','VVW1','VVW2','WCD','PMB1','ALS1','HMT1','SCR1','BCRK','BCR2','BFD1','CNR5','COD1','CRG1','SHCG',
        'TC01','CL01','DOWG','TLM2','EPS1','SCR6','FH1','ECO4','HRT4','JOF1','IOR3','PEC1','MEG1','MKRC','IOR1','MUL1','MKR1','IOR2','NXO2','SCR5','PR1','RL1','TCO2',
        'SDH1','APS1','IOR4','SCL1','UOC1','UOA1','ECO1','CAL1','FNG1','CMH1','NX01','EGC1','BR4','BR5','KH2','KH3','SH1','SH2','SD6','Unknown'),horizontal = True)
        name = ques
        st.write('You have selected',name,'. Please confirm that the dates: ', ss.dateRange[0], 'to ', ss.dateRange[1], 'are correct. If these dates are not correct, please press the reset button now. ' )
        button_Submit = st.button("Submit")
        startDate = ss.dateRange[0].strftime("%Y%m%d")
        endDate = ss.dateRange[-1].strftime("%Y%m%d")
        if button_Submit:
            button_finalChanges = st.button("Pressing this box will make these changes to the database. Are you Sure?")
            if button_finalChanges:
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
                cursor.execute('''
                            UPDATE gasAB
                            SET {0} = 0
                            WHERE DateNum >= ? AND DateNum <= ?'''.format(name),startDate,endDate)
                cursor.commit()
        
    if option =='Hydro':
        ques = st.radio("Pick available Coal plants:",('BIG','BOW1','BRA','CHIN','DKSN','ICP1','OMRH','RYMD','TAY1','Unknown'),horizontal = True)
        name = ques
        st.write('You have selected',name,'. Please confirm that the dates: ', ss.dateRange[0], 'to ', ss.dateRange[1], 'are correct. If these dates are not correct, please press the reset button now. ' )
        button_Submit = st.button("Submit")
        startDate = ss.dateRange[0].strftime("%Y%m%d")
        endDate = ss.dateRange[-1].strftime("%Y%m%d")
        if button_Submit:
            button_finalChanges = st.button("Pressing this box will make these changes to the database. Are you Sure?")
            if button_finalChanges:
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
                cursor.execute('''
                            UPDATE hydroAB
                            SET {0} = 0
                            WHERE DateNum >= ? AND DateNum <= ?'''.format(name),startDate,endDate)
                cursor.commit()

    if option =='Intertie':
        ques = st.radio("Pick available Coal plants:",('BC_MATLIM','BCIM','MATLIM','SASKIM'),horizontal = True)
        name = ques
        st.write('You have selected',name,'. Please confirm that the dates: ', ss.dateRange[0], 'to ', ss.dateRange[1], 'are correct. If these dates are not correct, please press the reset button now. ' )
        button_Submit = st.button("Submit")
        startDate = ss.dateRange[0].strftime("%Y%m%d")
        endDate = ss.dateRange[-1].strftime("%Y%m%d")
        if button_Submit:
            button_finalChanges = st.button("Pressing this box will make these changes to the database. Are you Sure?")
            if button_finalChanges:
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
                cursor.execute('''
                            UPDATE intertieAB
                            SET {0} = 0
                            WHERE DateNum >= ? AND DateNum <= ?'''.format(name),startDate,endDate)
                cursor.commit()

    if option =='Energy':
        ques = st.radio("Pick available Coal plants:",('SUM1','ERV1','ERV2','ERV3','Unknown'),horizontal = True)
        name = ques
        st.write('You have selected',name,'. Please confirm that the dates: ', ss.dateRange[0], 'to ', ss.dateRange[1], 'are correct. If these dates are not correct, please press the reset button now. ' )
        button_Submit = st.button("Submit")
        startDate = ss.dateRange[0].strftime("%Y%m%d")
        endDate = ss.dateRange[-1].strftime("%Y%m%d")
        if button_Submit:
            button_finalChanges = st.button("Pressing this box will make these changes to the database. Are you Sure?")
            if button_finalChanges:
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
                cursor.execute('''
                            UPDATE energyAB
                            SET {0} = 0
                            WHERE DateNum >= ? AND DateNum <= ?'''.format(name),startDate,endDate)
                cursor.commit()
    if option =='Other':
        ques = st.radio("Pick available Other plants:",('AFG1','BON1','CCMH','DAI1','GOC1','GPEC','NRG3','SLP1','SRL1','WWD1','WST1','WEY1','EAGL','Unknown'),horizontal = True)
        name = ques
        st.write('You have selected',name,'. Please confirm that the dates: ', ss.dateRange[0], 'to ', ss.dateRange[1], 'are correct. If these dates are not correct, please press the reset button now. ' )
        button_Submit = st.button("Submit")
        startDate = ss.dateRange[0].strftime("%Y%m%d")
        endDate = ss.dateRange[-1].strftime("%Y%m%d")
        if button_Submit:
            button_finalChanges = st.button("Pressing this box will make these changes to the database. Are you Sure?")
            if button_finalChanges:
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
                cursor.execute('''
                            UPDATE otherAB
                            SET {0} = 0
                            WHERE DateNum >= ? AND DateNum <= ?'''.format(name),startDate,endDate)
                cursor.commit()

    if option =='Dual Fuel':
        ques = st.radio("Pick available Duel Fuel plants:",('GN3','zilch'),horizontal = True)
        name = ques
        st.write('You have selected',name,'. Please confirm that the dates: ', ss.dateRange[0], 'to ', ss.dateRange[1], 'are correct. If these dates are not correct, please press the reset button now. ' )
        button_Submit = st.button("Submit")
        startDate = ss.dateRange[0].strftime("%Y%m%d")
        endDate = ss.dateRange[-1].strftime("%Y%m%d")
        if button_Submit:
            button_finalChanges = st.button("Pressing this box will make these changes to the database. Are you Sure?")
            if button_finalChanges:
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
                cursor.execute('''
                            UPDATE dualfuelAB
                            SET {0} = 0
                            WHERE DateNum >= ? AND DateNum <= ?'''.format(name),startDate,endDate)
                cursor.commit()

    if option =='Solar':
        ques = st.button("Solar is all under one header: Press this button to set insert function to True.")
        name = ques
        st.write('You have selected',name,'. Please confirm that the dates: ', ss.dateRange[0], 'to ', ss.dateRange[1], 'are correct. If these dates are not correct, please press the reset button now. ' )
        button_Submit = st.button("Submit")
        startDate = ss.dateRange[0].strftime("%Y%m%d")
        endDate = ss.dateRange[-1].strftime("%Y%m%d")
        if button_Submit:
            button_finalChanges = st.button("Pressing this box will make these changes to the database. Are you Sure?")
            if button_finalChanges:
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
                cursor.execute('''
                            UPDATE solarAB
                            SET {0} = 0
                            WHERE DateNum >= ? AND DateNum <= ?'''.format(name),startDate,endDate)
                cursor.commit()
    if option =='Wind':
        quesb = st.button("Wind is all under one header: Press this button to set insert function to True.")
        name = quesb
        st.write('You have selected',name,'. Please confirm that the dates: ', ss.dateRange[0], 'to ', ss.dateRange[1], 'are correct. If these dates are not correct, please press the reset button now. ' )
        button_Submit = st.button("Submit")
        startDate = ss.dateRange[0].strftime("%Y%m%d")
        endDate = ss.dateRange[-1].strftime("%Y%m%d")
        if button_Submit:
            button_finalChanges = st.button("Pressing this box will make these changes to the database. Are you Sure?")
            if button_finalChanges:
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
                cursor.execute('''
                            UPDATE windAB
                            SET {0} = 0
                            WHERE DateNum >= ? AND DateNum <= ?'''.format(name),startDate,endDate)
                cursor.commit()






