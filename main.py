import streamlit as st
import pandas as pd

file_path = 'final_merged_data.csv'

try:
    data = pd.read_csv(file_path)
except FileNotFoundError:
    st.error('car_data.csv file not found. Please make sure it is located in the correct directory.')
    st.stop()
    
def filter_data(name, award, country, gdp_per_capita, household_spending):
    filtered_data = data
    if name:
        filtered_data = filtered_data[filtered_data['Name'].str.contains(name, case=False)]
    if country: 
        filtered_data = filtered_data[filtered_data['Country'].str.contains(country, case=False)]
    if award:
        filtered_data = filtered_data[filtered_data['Award'].isin(award)]
    filtered_data = filtered_data[
        (filtered_data['GDP per Capita (USD)'] >= gdp_per_capita[0]) &
        (filtered_data['GDP per Capita (USD)'] <= gdp_per_capita[1])
    ]
    filtered_data = filtered_data[
        (filtered_data['Household Spending (Million US$)'] >= household_spending[0]) &
        (filtered_data['Household Spending (Million US$)'] <= household_spending[1])
    ]
    return filtered_data

st.sidebar.header('Filter Options')
name = st.sidebar.text_input('Name')
country = st.sidebar.text_input('Country')
award = st.sidebar.multiselect('Award', ['3 Stars', '2 Stars', '1 Star', 'Bib Gourmand'], default=['3 Stars', '2 Stars', '1 Star', 'Bib Gourmand'])
gdp_per_capita = st.sidebar.slider('GDP per Capita (USD)', 6923, 116906, (6923, 116906))
household_spending = st.sidebar.slider('Household Spending', 12775, 15902575, (12775, 15902575))

if st.sidebar.button('Submit'):
    filtered_data = filter_data(name, award, country, gdp_per_capita, household_spending)
    st.write(filtered_data)
else:
    st.write(data)

