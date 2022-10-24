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
from azure.storage.blob import BlobServiceClient
from azure.storage.blob import BlobClient
from azure.storage.blob import ContainerClient
import pandas as pd
import asyncio

st.set_page_config(page_title="Dahlia", page_icon="random", layout="wide", initial_sidebar_state="expanded")
st.title("Dahlia")
import time




    # 
blob_service_client = BlobServiceClient.from_connection_string("DefaultEndpointsProtocol=https;AccountName=suncoravailabilityblob;AccountKey=xyH38moVc3iB9kCMxbgP4pCTLePm887BSqBNjjDLEsDRUC7MCSbxFp3hu6lUmOjLyCa57uVD2ii1+ASt//oE2w==;EndpointSuffix=core.windows.net")
container_client = blob_service_client.get_container_client("90dayevent")
blobs_list = container_client.list_blobs()
for blob in blobs_list:
    print(blob.name + '\n')
with st.container():
    mystyle = '''
        <style>
            p {
                text-align: justify;
            }
        </style>
        '''

    st.markdown(mystyle, unsafe_allow_html=True)

    if not 'todolist' in st.session_state:
        st.session_state.todolist = []
    col1,col2,col3,col4=st.columns((2,1,1,1))


    blob_client = BlobClient.from_blob_url(blob_url="https://suncoravailabilityblob.blob.core.windows.net/events7day/7day.csv")


    df = blob_client.download_blob()


    df = pd.read_csv(df)

    col1.dataframe(df)




    blob_service_client = BlobServiceClient.from_connection_string("DefaultEndpointsProtocol=https;AccountName=suncoravailabilityblob;AccountKey=xyH38moVc3iB9kCMxbgP4pCTLePm887BSqBNjjDLEsDRUC7MCSbxFp3hu6lUmOjLyCa57uVD2ii1+ASt//oE2w==;EndpointSuffix=core.windows.net")
    container_client = blob_service_client.get_container_client("seveneventstream")
    eventlist = []
    blobs_list = container_client.list_blobs()
    for blob in blobs_list:
        blobs = blob.name
        eventlist.append(blobs)
        print(blob.name + '\n')
    number_of_blobs = len(list(blobs_list))


    DF_list = list()
    for i in range(0,len(list(eventlist))):
        blob_client = container_client.get_blob_client(eventlist[i])
        dfupdate = blob_client.download_blob()
        dfupdate = pd.read_csv(dfupdate)
        DF_list.append(dfupdate)
    for i in range(0,len(list(DF_list))):
        col2.dataframe(DF_list[i])
        dbb = col3.checkbox(eventlist[i])
        if dbb:
            col4.write('Selected!')
    col4.button('Eliminate Seven Day')       
######################################
with st.container():
    mystyle = '''
        <style>
            p {
                text-align: justify;
            }
        </style>
        '''

    st.markdown(mystyle, unsafe_allow_html=True)

    if not 'todolist' in st.session_state:
        st.session_state.todolist = []
    col1,col2,col3,col4=st.columns((2,1,1,1))


    blob_client = BlobClient.from_blob_url(blob_url="https://suncoravailabilityblob.blob.core.windows.net/event90day/90day.csv")
    df = blob_client.download_blob()
    df = pd.read_csv(df)
    col1.dataframe(df)
    blob_service_client = BlobServiceClient.from_connection_string("DefaultEndpointsProtocol=https;AccountName=suncoravailabilityblob;AccountKey=xyH38moVc3iB9kCMxbgP4pCTLePm887BSqBNjjDLEsDRUC7MCSbxFp3hu6lUmOjLyCa57uVD2ii1+ASt//oE2w==;EndpointSuffix=core.windows.net")
    container_client = blob_service_client.get_container_client("90dayevent")
    eventlist = []
    blobs_list = container_client.list_blobs()
    for blob in blobs_list:
        blobs = blob.name
        eventlist.append(blobs)
        print(blob.name + '\n')
    number_of_blobs = len(list(blobs_list))


    DF_list = list()
    for i in range(0,len(list(eventlist))):
        blob_client = container_client.get_blob_client(eventlist[i])
        dfupdate = blob_client.download_blob()
        dfupdate = pd.read_csv(dfupdate)
        DF_list.append(dfupdate)
    for i in range(0,len(list(DF_list))):
        col2.dataframe(DF_list[i])
        dbb = col3.checkbox(eventlist[i])
        if dbb:
            col4.write('Selected!')
    col4.button('Eliminate Daily')
with st.container():
    mystyle = '''
        <style>
            p {
                text-align: justify;
            }
        </style>
        '''

    st.markdown(mystyle, unsafe_allow_html=True)

    if not 'todolist' in st.session_state:
        st.session_state.todolist = []
    col1,col2,col3,col4=st.columns((2,1,1,1))


    blob_client = BlobClient.from_blob_url(blob_url="https://suncoravailabilityblob.blob.core.windows.net/eventmonthly/monthly.csv")
    df = blob_client.download_blob()
    df = pd.read_csv(df)
    col1.dataframe(df)
    blob_service_client = BlobServiceClient.from_connection_string("DefaultEndpointsProtocol=https;AccountName=suncoravailabilityblob;AccountKey=xyH38moVc3iB9kCMxbgP4pCTLePm887BSqBNjjDLEsDRUC7MCSbxFp3hu6lUmOjLyCa57uVD2ii1+ASt//oE2w==;EndpointSuffix=core.windows.net")
    container_client = blob_service_client.get_container_client("monthlyeventstream")
    eventlist = []
    blobs_list = container_client.list_blobs()
    for blob in blobs_list:
        blobs = blob.name
        eventlist.append(blobs)
        print(blob.name + '\n')
    number_of_blobs = len(list(blobs_list))


    DF_list = list()
    for i in range(0,len(list(eventlist))):
        blob_client = container_client.get_blob_client(eventlist[i])
        dfupdate = blob_client.download_blob()
        dfupdate = pd.read_csv(dfupdate)
        DF_list.append(dfupdate)
    for i in range(0,len(list(DF_list))):
        col2.dataframe(DF_list[i])
        dbb = col3.checkbox(eventlist[i])
        if dbb:
            col4.write('Selected!')
    col4.button('Eliminate Monthly')

async def periodic():
    while True:
        
        r = await asyncio.sleep(1)
        st.write(f"asyncio sleep ? {r}")

asyncio.run(periodic())