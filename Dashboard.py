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

    # Vessels
    st.header('Vessels')
    st.dataframe(vessels_df)

    st.bar_chart(pd.DataFrame(
    {'Current Quantity': vessels_df['Current Quantity'].values,
        'Max Quantity': vessels_df['Max Quantity'].values},
    index=vessels_df['Fleet and Vessel type']), horizontal=True)

    # Land Equipment
    st.header('Land Equipment')
    st.dataframe(land_equipment_df)

    st.bar_chart(pd.DataFrame(
    {'Current Quantity': land_equipment_df['Current Quantity'].values,
        'Max Quantity': land_equipment_df['Max Quantity'].values},
    index=land_equipment_df['Platform type and platform']), horizontal=True)

    # Aircraft
    st.header('Aircraft')
    st.dataframe(aircraft_df)

    st.bar_chart(pd.DataFrame(
    {'Current Quantity': aircraft_df['Current Quantity'].values,
        'Max Quantity': aircraft_df['Max Quantity'].values},
    index=aircraft_df['Platform Type']), horizontal=True)

    # Helicopters
    st.header('Helicopters')
    st.dataframe(rotor_df)

    st.bar_chart(pd.DataFrame(
        {'Current Quantity': rotor_df['Current Quantity'].values,
         'Max Quantity': rotor_df['Max Quantity'].values},
        index=rotor_df['Platform Type']), horizontal=True)
    
