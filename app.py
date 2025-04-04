import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime,date
import requests

'''
# TaxiFareModel front
'''

st.markdown('''
Remember that there are several ways to output content into your web page...

Either as with the title by just creating a string (or an f-string). Or as with this paragraph using the `st.` functions
''')

'''
## Here we would like to add some controllers in order to ask the user to select the parameters of the ride

1. Let's ask for:
- date and time
- pickup longitude
- pickup latitude
- dropoff longitude
- dropoff latitude
- passenger count
'''

'''
## Once we have these, let's call our API in order to retrieve a prediction

See ? No need to load a `model.joblib` file in this app, we do not even need to know anything about Data Science in order to retrieve a prediction...

🤔 How could we call our API ? Off course... The `requests` package 💡
'''

url = 'https://taxifare.lewagon.ai/predict'

if url == 'https://taxifare.lewagon.ai/predict':

    st.markdown('Maybe you want to use your own API for the prediction, not the one provided by Le Wagon...')

'''

2. Let's build a dictionary containing the parameters for our API...

3. Let's call our API using the `requests` package...

4. Let's retrieve the prediction from the **JSON** returned by the API...

## Finally, we can display the prediction to the user
'''
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
        st.error(f"Error al enviar los datos a la API: {response.status_code}")