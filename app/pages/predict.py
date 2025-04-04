import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime,date
import requests

params = st.query_params


if 'date' in params:
    pickup_datetime = datetime.strptime(params['date'][0], "%Y-%m-%d").date()
else:
    pickup_datetime = datetime.today().date()

if 'time' in params:
    pickup_time = datetime.strptime(params['time'][0], "%H:%M:%S").time()
else:
    pickup_time = datetime(1900, 1, 1, 12, 0, 0).time() 
st.subheader('1. Date and time')
min_date = date(2009, 1, 1)
pickup_datetime = st.date_input('Select the date:', value=pickup_datetime, min_value=min_date)
pickup_time_str = st.text_input('Select the time', value=pickup_time.strftime('%H:%M:%S'))
st.subheader('2. Coords to pick up')
pickup_lat = st.number_input('Lat of pick up', value=40.7128)
pickup_lon = st.number_input('Lon of pick up', value=-74.0060)
st.subheader('3. Coords to drop off')
dropoff_lat = st.number_input('Lat of drop off', value=40.730610)
dropoff_lon = st.number_input('Lon of drop off', value=-73.935242)
st.subheader('4. Number of passengers')
passenger_count = st.number_input('Number of passengers', min_value=1, max_value=8, value=1)

api_url = "https://taxifare-884199091247.us-south1.run.app/predict"
if st.button('Predict'):
    formatted_datetime = f"{pickup_datetime.strftime('%Y-%m-%d')} {pickup_time_str}"
    params = {
    "pickup_datetime": formatted_datetime, 
    "pickup_latitude": pickup_lat,
    "pickup_longitude": pickup_lon,
    "dropoff_longitude": dropoff_lon,
    "dropoff_latitude": dropoff_lat,
    "passenger_count": passenger_count
}
    response = requests.get(api_url, params=params)

    if response.status_code == 200:
        st.success("Data sent correctly to the API")
        st.write('Amount to pay is:',response.json()["fare"])  
    else:
        st.error(f"Error to sent the data: {response.status_code}")