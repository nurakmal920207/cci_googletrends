#!/usr/bin/env python
# coding: utf-8


import pandas as pd
import streamlit as st
import plotly.express as px
from datetime import datetime
import io

st.set_page_config(layout="wide")

st.title('Google Trends Dashboard')

df_chart = pd.read_excel('for_chart.xlsx')

region_list = ['Global', 'Arab States', 'Africa', 'South/Latin America', 'Asia & Pacific', 'Europe', 'North America', 'Middle east']
country_list = df_chart['Country'].unique().tolist()
country_list.remove('Global Average')
country = st.sidebar.multiselect('Select countries:', country_list)
averages = {}
st.sidebar.write('Averages:')
for region in region_list:
    averages[region] = st.sidebar.checkbox(region)
first_date = datetime.strptime(df_chart['Date'].values.tolist()[0], '%Y-%m-%d')
last_date = datetime.strptime(df_chart['Date'].values.tolist()[-1], '%Y-%m-%d')
date_slider = st.slider('Date Range Selector:', first_date, last_date, (first_date, last_date))
color_dict = {}
for i,x in enumerate(country):
    color_dict[x] = px.colors.qualitative.Dark24[i]
    
averages_list = [f'{k} Average' for k, v in averages.items() if v]
country.extend(averages_list)

try:
    df_filter = df_chart[df_chart['Country'].isin(country)]
    df_filter = df_filter.loc[(df_filter['Date'] >= date_slider[0].strftime('%Y-%m-%d')) & (df_filter['Date'] <= date_slider[1].strftime('%Y-%m-%d'))]
    x = df_filter['Date'].values.tolist()
    y = df_filter['Score'].values.tolist()
    
    fig = px.line(df_filter, x = x, y = y,
                  labels = {'x': 'Date', 'y':'Score'}, color = 'Country')
    
    #fix the y-axis
    fig.update_layout(yaxis_range=[65,135])
    
    fig.for_each_trace(lambda trace: trace.update(line=dict(width=4)) if 'Average' in trace.name else(),)
    
    st.plotly_chart(fig, use_container_width=True)
    
except:
    st.write('Please select a country')
    
df_pivot = df_filter.pivot(index='Country', columns='Date', values='Score')

buffer = io.BytesIO()

# Create a Pandas Excel writer using XlsxWriter as the engine.
with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
    # Write each dataframe to a different worksheet.
    df_pivot.to_excel(writer, sheet_name='Sheet1')


    # Close the Pandas Excel writer and output the Excel file to the buffer
    writer.save()

    st.download_button(
        label="Download Excel worksheets",
        data=buffer,
        file_name="Google Trends Dashboard Data.xlsx",
        mime="application/vnd.ms-excel"
    )

# try:
#     if global_average:
#         country.extend(['Global Average'])
#         color_dict['Global Average'] = 'grey'
#         df_filter = df_chart[df_chart['Country'].isin(country)]
#         df_filter = df_filter.loc[(df_filter['Date'] >= date_slider[0].strftime('%Y-%m-%d')) & (df_filter['Date'] <= date_slider[1].strftime('%Y-%m-%d'))]
#         x = df_filter['Date'].values.tolist()
#         y = df_filter['Score'].values.tolist()
        
#         fig = px.line(df_filter, x = x, y = y, 
#                       labels = {'x': 'Date', 'y':'Score'}, color = 'Country', color_discrete_map = color_dict)
        
#         #fix the y-axis
#         fig.update_layout(yaxis_range=[70,130])
        
#         fig.for_each_trace(lambda trace: trace.update(line=dict(width=4)) if trace.name == "Global Average" else(),)
        
#         st.plotly_chart(fig, use_container_width=True)
        
#     else:
#         df_filter = df_chart[df_chart['Country'].isin(country)]
#         df_filter = df_filter.loc[(df_filter['Date'] >= date_slider[0].strftime('%Y-%m-%d')) & (df_filter['Date'] <= date_slider[1].strftime('%Y-%m-%d'))]
#         x = df_filter['Date'].values.tolist()
#         y = df_filter['Score'].values.tolist()
        
#         fig = px.line(df_filter, x = x, y = y,
#                       labels = {'x': 'Date', 'y':'Score'}, color = 'Country')
        
#         #fix the y-axis
#         fig.update_layout(yaxis_range=[70,130])
        
#         fig.for_each_trace(lambda trace: trace.update(line=dict(width=4)) if trace.name == "Global Average" else(),)
    
#         st.plotly_chart(fig, use_container_width=True)


    






