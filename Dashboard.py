import streamlit as st
import pandas as pd
import math
import re
import copy
from millify import millify

def calculate_budget(dataframe, budget):
    dataframe['Purchasable'] = (budget / dataframe['Unit Cost']).apply(math.floor)
    dataframe['Max Quantity'] = dataframe['Current Quantity'] + dataframe['Purchasable']

def format_dataframe(dataframe):
    new_df = copy.copy(dataframe)
    new_df['Unit Cost'] = new_df['Unit Cost'].apply(lambda x: millify(x, precision=2))
    return new_df

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
    {'Current Quantity': vessels_df['Current Quantity'].values,
        'Max Quantity': vessels_df['Max Quantity'].values},
    index=vessels_df['Fleet and Vessel type']), horizontal=True)

    # Land Equipment
    st.header('Land Equipment')
    st.dataframe(format_dataframe(land_equipment_df))

    st.bar_chart(pd.DataFrame(
    {'Current Quantity': land_equipment_df['Current Quantity'].values,
        'Max Quantity': land_equipment_df['Max Quantity'].values},
    index=land_equipment_df['Platform type and platform']), horizontal=True)

    # Aircraft
    st.header('Aircraft')
    st.dataframe(format_dataframe(aircraft_df))

    st.bar_chart(pd.DataFrame(
    {'Current Quantity': aircraft_df['Current Quantity'].values,
        'Max Quantity': aircraft_df['Max Quantity'].values},
    index=aircraft_df['Platform Type']), horizontal=True)

    # Helicopters
    st.header('Helicopters')
    st.dataframe(format_dataframe(rotor_df))

    st.bar_chart(pd.DataFrame(
        {'Current Quantity': rotor_df['Current Quantity'].values,
         'Max Quantity': rotor_df['Max Quantity'].values},
        index=rotor_df['Platform Type']), horizontal=True)