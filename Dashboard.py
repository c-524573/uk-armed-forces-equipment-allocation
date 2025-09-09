import streamlit as st
import pandas as pd
import math

def calculate_budget(dataframe, budget):
    dataframe['Purchasable'] = (budget / dataframe['Unit Cost']).apply(math.floor)
    dataframe['Max Quantity'] = dataframe['Current Quantity'] + dataframe['Purchasable']

st.title('UK Armed Forces Equipment Allocation')

# Load Datasets
vessels_df = pd.read_csv('Dataset/vessels.csv')
land_equipment_df = pd.read_csv('Dataset/land_equipment.csv')
aircraft_df = pd.read_csv('Dataset/aircraft.csv')
rotor_df = pd.read_csv('Dataset/rotor.csv')

# Value input
budget = st.number_input('Enter Budget:', value=4700000000)
if st.button('Calculate'):

    # Calculate Budget
    calculate_budget(vessels_df, budget=budget)
    calculate_budget(land_equipment_df, budget=budget)
    calculate_budget(aircraft_df, budget=budget)
    calculate_budget(rotor_df, budget=budget)

    # Display Datasets
    st.subheader('Vessels')
    st.dataframe(vessels_df)

    st.subheader('Land Equipment')
    st.dataframe(land_equipment_df)

    st.subheader('Aircraft')
    st.dataframe(aircraft_df)

    st.subheader('Helicopters')
    st.dataframe(rotor_df)

    st.bar_chart(pd.concat([vessels_df['Fleet and Vessel type'], vessels_df['Current Quantity']], axis=1), horizontal=True)