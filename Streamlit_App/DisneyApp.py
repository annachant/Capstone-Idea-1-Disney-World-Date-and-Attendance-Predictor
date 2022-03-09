import os
from pathlib import Path
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from PIL import Image

# def img_to_bytes(img_path):
#     img_bytes = Path(img_path).read_bytes()
#     encoded = base64.b64encode(img_bytes).decode()
#     return encoded

# header_html = "<img src='https://github.com/annachant/Capstone-Disney-World-Date-and-Attendance-Predictor/blob/main/images/banner5.jpeg' class='img-fluid'>".format(
#     img_to_bytes("header.png")
# )
# st.markdown(
#     header_html, unsafe_allow_html=True,
# )


pd.set_option("display.max_rows", None, "display.max_columns", None)

datapath = Path.cwd() 
print(datapath)

datasets = os.listdir(datapath)
datasets = list(sorted([i for i in datasets if ".csv" in i]))
print(datasets)

for i in datasets:
    try:
        print(i)
        exec(f"{i.split('.csv')[0]} = pd.read_csv(datapath / i)")
    except:
        print(f"{i} cannot be imported automatically")



#Add sidebar to the app
st.sidebar.markdown("### Aloha!")
st.sidebar.markdown("Welcome to the Disney Day app! This app is designed to predict whether the day you would like to go to a particular park in Disney World is a good day to go! This app uses data sourced from touringplans.com. I hope you enjoy!")

#Add title and subtitle to the main interface of the app
st.title("Walt Disney World Predictor")
st.markdown("Did you know that there are 58 million people that go to Disney World in Orlando, FL every year? It is no secret that some days are incredibly busier than others and lines can seem like a mile long. Visitors spend tons of money to provide an unforgettable experience for their family and want to have a great time. Depending on the time of year you go, that experience can be absolutely magnificient, if the timing is great! I want you to have that same unforgettable experience!")
st.markdown("Input the date of your planned visit, along with the park you would like to attend. The algorithm will work its magic and tell you whether it is a great day to go, or not!")

parks = []
for i in datasets:
    name = i.split(".csv")[0].split("_")[3:]
    name = [j[0].upper()+ j[1:] for j in name]
    name = " ".join(name)
    # print(name)
    parks.append(name)

selected_park = st.selectbox("Select Park", parks)


park_idx = parks.index(selected_park) 
best_days = eval(f'{datasets[park_idx].split(".csv")[0]}')
dates = list(best_days["ds"])
now = datetime.now()
date = now
dates = []
while date <= now + timedelta(weeks= 52):
    dates.append(f'{date.year}-{date.month}-{date.day}')
    date += timedelta(days = 1)
selected_date = st.selectbox("Select Date", dates)
    

best_metrics = best_days.groupby(by = ['month', 'week', 'weekday']).count();
# display(best_metrics.sort_values('y', ascending = False))
# display(best_metrics)


dt = datetime.strptime(selected_date, '%Y-%m-%d')
month = dt.month
week = dt.isocalendar()[1]
day = dt.weekday()
print(month, week, day)

try:
    best_metrics.loc[month, week, day]
    print(f'{selected_date} is a good day to go to the park!')
    st.markdown(f'{selected_date} is a good day to go to the park!')
except KeyError:
    print(f'{selected_date} is a bad day to go to the park!')
    st.markdown(f'{selected_date} is a bad day to go to the park!')


