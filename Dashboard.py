import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import math
import re
import copy
from millify import millify

st.set_page_config(layout='wide')

def calculate_budget(dataframe, budget):
    dataframe['New Units'] = (budget / dataframe['Unit Cost']).apply(math.floor)
    dataframe['Updated Units'] = dataframe['Current Units'] + dataframe['New Units']

def format_dataframe(dataframe):
    new_df = copy.copy(dataframe)
    new_df['Unit Cost'] = new_df['Unit Cost'].apply(lambda x: millify(x, precision=2))
    return new_df.rename(columns={'Unit Cost': 'Unit Cost*',
                                  'Current Units': 'Current Units (2024)',
                                  'Historical Units': 'Historical Units (2016)'})

def dumbbell_chart(dataframe, equipment_title):
    equipment = dataframe[equipment_title]
    historical = dataframe['Historical Units']
    current = dataframe['Current Units']

    fig = go.Figure()

    for _, row in dataframe.iterrows():
        fig.add_trace(go.Scatter(
            x=[row['Historical Units'], row['Current Units']],
            y=[row[equipment_title], row[equipment_title]],
            mode='lines',
            line={'color': 'lightgray', 'width': 2},
            showlegend=False
        ))

    fig.add_trace(go.Scatter(
        x=dataframe['Historical Units'],
        y=dataframe[equipment_title],
        mode='markers',
        name='Historical Units (2016)',
        marker={'color': 'blue', 'size': 12}
    ))

    fig.add_trace(go.Scatter(
        x=dataframe['Current Units'],
        y=dataframe[equipment_title],
        mode='markers',
        name='Current Units (2024)',
        marker={'color': 'red', 'size': 12}
    ))

    return fig


st.title('UK Armed Forces Equipment Allocation')

# Load Datasets
vessels_df = pd.read_csv('Dataset/vessels.csv')
land_equipment_df = pd.read_csv('Dataset/land_equipment.csv')
aircraft_df = pd.read_csv('Dataset/aircraft.csv')
rotor_df = pd.read_csv('Dataset/rotor.csv')

# Value input
budget = st.text_input('Enter Budget:', value='4.7B').lower()

if st.button('Calculate'):
    if len(re.findall('^[0-9]+(?:\.[0-9]+)?[kmb]$', budget)) <= 0:
        st.error('Error: Budget not in correct format, correct formats: 10k, 7.5m, or 31.45b')

    if 'k' in budget:
        budget = float(budget[:-1]) * 1000
    elif 'm' in budget:
        budget = float(budget[:-1]) * 1_000_000
    elif 'b' in budget:
        budget = float(budget[:-1]) * 1_000_000_000

    # Calculate Budget
    calculate_budget(vessels_df, budget=budget)
    calculate_budget(land_equipment_df, budget=budget)
    calculate_budget(aircraft_df, budget=budget)
    calculate_budget(rotor_df, budget=budget)

    # Vessels
    st.header('Vessels')
    st.dataframe(format_dataframe(vessels_df))

    st.bar_chart(pd.DataFrame(
    {'Current Units': vessels_df['Current Units'].values,
        'New Units': vessels_df['New Units'].values},
    index=vessels_df['Fleet and Vessel type']), horizontal=True)

    st.subheader('Historical (2016) vs Current (2024) Equipment')
    st.plotly_chart(dumbbell_chart(vessels_df, equipment_title='Fleet and Vessel type'), use_container_width=True)

    # Land Equipment
    st.header('Land Equipment')
    st.dataframe(format_dataframe(land_equipment_df))

    st.bar_chart(pd.DataFrame(
    {'Current Units': land_equipment_df['Current Units'].values,
        'New Units': land_equipment_df['New Units'].values},
    index=land_equipment_df['Platform type and platform']), horizontal=True)

    st.subheader('Historical (2016) vs Current (2024) Equipment')
    st.plotly_chart(dumbbell_chart(land_equipment_df, equipment_title='Platform type and platform'), use_container_width=True)

    # Aircraft
    st.header('Aircraft')
    st.dataframe(format_dataframe(aircraft_df))

    st.bar_chart(pd.DataFrame(
    {'Current Units': aircraft_df['Current Units'].values,
        'New Units': aircraft_df['New Units'].values},
    index=aircraft_df['Platform Type']), horizontal=True)

    st.subheader('Historical (2016) vs Current (2024) Equipment')
    st.plotly_chart(dumbbell_chart(aircraft_df, equipment_title='Platform Type'), use_container_width=True)

    # Helicopters
    st.header('Helicopters')
    st.dataframe(format_dataframe(rotor_df))

    st.bar_chart(pd.DataFrame(
        {'Current Units': rotor_df['Current Units'].values,
         'New Units': rotor_df['New Units'].values},
        index=rotor_df['Platform Type']), horizontal=True)
    
    st.subheader('Historical (2016) vs Current (2024) Equipment')
    st.plotly_chart(dumbbell_chart(rotor_df, equipment_title='Platform Type'), use_container_width=True)
    
    st.markdown('*\* Unit Cost is calculated from open source data so may be inaccurate.*')