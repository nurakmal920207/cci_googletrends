#!/usr/bin/env python
# coding: utf-8


import pandas as pd
import pickle
import streamlit as st
import io

buffer = io.BytesIO()

st.title('Consumer Confidence Index - Google Trends Simulator')

st.write('Hi Aruni, I developed this simple web app for you to freely run your simulation. You can play with the WEIGHTS below, and adjust the year that you want for the LONG TERM AVERAGE calculation. When you are done, click "Submit", and the app will calculate the result for you!')

with open('dictionary.pickle', 'rb') as handle:
    dict_ = pickle.load(handle)

df = pd.read_csv('oecd_data.csv')

df.drop(['SUBJECT', 'Subject', 'LOCATION', 'FREQUENCY', 'Frequency', 'TIME', 'Unit Code', 'Unit', 'PowerCode Code', 'PowerCode', 'Reference Period Code', 'Reference Period', 'Flag Codes', 'Flags'], axis=1, inplace=True)

df['Time'] = pd.to_datetime(df['Time'])

df['Date'] = df['Time']
df.drop(['Time'], axis=1, inplace=True)

df_corr = pd.DataFrame(index=dict_['Australia'].columns)

for country in dict_.keys():
    if (country in df['Country'].tolist()):
        dict_[country]['Date'] = pd.to_datetime(dict_[country]['Date'])
        dict_[country].replace('<1', 1, inplace = True)
        df_merge = pd.merge(dict_[country],df[df['Country'] == country], on='Date')
        df_merge.drop(['Date', 'Country'], axis = 1, inplace = True)
        corr = df_merge.astype(float).corrwith(df_merge['Value'], method='pearson')
        df_corr[country] = corr

df_corr.drop(['Date'],axis=0,inplace=True)


#df_corr.to_excel('output.xlsx')


df_weight = pd.read_csv('weight.csv', index_col = 'Category')

category = df_weight.index.tolist()

data= []

with st.form(key = 'weight'):
    for i,x in enumerate(category):
        data.append(st.number_input(x,key = str(i), value = df_weight.iloc[i].tolist()[0]))
    
    year_start_end = st.slider(label='Year Selection for Long Term Average', min_value=2005, max_value=2022, value=[2009,2019], step=1)
        
    submit_button = st.form_submit_button(label='Submit')
#data = np.array(data).tolist()
df_weight['Weight'] = data

df_corr_weight = pd.DataFrame(index = [country for country in dict_.keys() if country in df['Country'].tolist()], columns = [date for date in df['Date'].unique()])

please_wait = st.empty()
please_wait.text('Calculating results. Please wait...')
#calculate for correlation * month
new_columns = df_weight.index.tolist()
new_columns.append('Date')
for country in df_corr_weight.index:
    df_merge = pd.merge(dict_[country],df[df['Country'] == country], on='Date')  
    df_merge = df_merge[new_columns]
    for date in df['Date'].unique():
        df_merge_date = df_merge.loc[df_merge['Date'] == date]
        df_transpose = df_merge_date.transpose()
        try:
            df_transpose.columns = ['Date']
            df_transpose_merge = df_weight.merge(df_transpose, left_index=True, right_index=True)
            df_transpose_merge['Product'] = df_transpose_merge['Weight'] * df_transpose_merge['Date']
            df_corr_weight.loc[country,date] = df_transpose_merge['Product'].sum()
        except:
            pass
please_wait.empty()
#with st.form(key = 'average'):
 #   year_start_end = st.slider(label='Year Selection for Long Term Average', min_value=2005, max_value=2022, value=[2009,2019], step=1)
  #  submit_button = st.form_submit_button(label='Submit')
        

df_corr_weight.columns = df_corr_weight.columns.map(lambda t: t.strftime('%Y-%m-%d'))


df_corr_weight['Average'] = df_corr_weight.iloc[:, df_corr_weight.columns.get_loc(f'{year_start_end[0]}-01-01'):df_corr_weight.columns.get_loc(f'{year_start_end[0]}-12-01')+1].mean(axis=1)


df_corr_weight_final = df_corr_weight.copy()


df_corr_weight_final.iloc[:,:-1] = df_corr_weight_final.iloc[:,:-1].divide(df_corr_weight_final.iloc[:,-1], axis="index")


df_corr_weight_final.drop(['Average'], axis = 1, inplace = True)

st.write('This is the result from multiplication of the overall correlation and the monthly data. You can find the average at the end of each rows')
st.dataframe(df_corr_weight)

st.write('This is the final score where the result from above divided by the average')
st.dataframe(df_corr_weight_final)
#with pd.ExcelWriter('countries_by_month.xlsx') as writer:  
    #df_corr_weight.to_excel(writer, sheet_name='Calculation')
    #df_corr_weight_final.to_excel(writer, sheet_name='Final Score')

with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
    # Write each dataframe to a different worksheet.
    df_corr_weight_final.to_excel(writer, sheet_name='Final Score')
    df_corr_weight.to_excel(writer, sheet_name='Calculation')
    
    # Close the Pandas Excel writer and output the Excel file to the buffer
    writer.save()

    st.download_button(
        label="Download Excel worksheets",
        data=buffer,
        file_name="countries_by_months.xlsx",
        mime="application/vnd.ms-excel"
    )
    






