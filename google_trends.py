#!/usr/bin/env python
# coding: utf-8


import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(layout="wide")

st.title('Google Trends Dashboard')

df_chart = pd.read_excel('for_chart.xlsx')

country_list = df_chart['Country'].unique()
country = st.sidebar.multiselect('Select countries:', country_list)

try:
    df_filter = df_chart[df_chart['Country'].isin(country)]
    x = df_filter['Date'].values.tolist()
    y = df_filter['Score'].values.tolist()
    
    fig = px.line(df_filter, x = x, y = y,
                  labels = {'x': 'Date', 'y':'Score'}, color = 'Country')

    st.plotly_chart(fig, use_container_width=True)

except:
    st.write('Please select a country')
    






