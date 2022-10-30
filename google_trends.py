#!/usr/bin/env python
# coding: utf-8


import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(layout="wide")

st.title('Google Trends Dashboard')

df_chart = pd.read_excel('for_chart.xlsx')

country_list = df_chart['Country'].unique().tolist()
country_list.remove('Global Average')
country = st.sidebar.multiselect('Select countries:', country_list)
global_average = st.sidebar.checkbox('Global Average')
color_dict = {}
for i,x in enumerate(country):
    color_dict[x] = px.colors.qualitative.Dark24[i]

try:
    if global_average:
        country.extend(['Global Average'])
        line_dict = {}
        color_dict['Global Average'] = 'grey'
        for x in country:
            line_dict[x] = 'solid'
            line_dict['Global Average'] = 'dash'
        df_filter = df_chart[df_chart['Country'].isin(country)]
        x = df_filter['Date'].values.tolist()
        y = df_filter['Score'].values.tolist()
        
        fig = px.line(df_filter, x = x, y = y, 
                      labels = {'x': 'Date', 'y':'Score'}, color = 'Country', color_discrete_map = color_dict, line_dash = 'Country', line_dash_map = line_dict)
        
        st.plotly_chart(fig, use_container_width=True)
        
    else:
        df_filter = df_chart[df_chart['Country'].isin(country)]
        x = df_filter['Date'].values.tolist()
        y = df_filter['Score'].values.tolist()
        
        fig = px.line(df_filter, x = x, y = y,
                      labels = {'x': 'Date', 'y':'Score'}, color = 'Country')
    
        st.plotly_chart(fig, use_container_width=True)

except:
    st.write('Please select a country')
    






