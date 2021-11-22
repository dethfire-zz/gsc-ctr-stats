import pandas as pd
import numpy as np
import streamlit as st
import base64

st.markdown("""
<style>
.big-font {
    font-size:40px !important;
}
</style>
""", unsafe_allow_html=True)


st.markdown("""
<p class="big-font">CTR Stats by GSC Position</p>
<b>Directions: </b></ br><ol>
<li>Export Performance data (impressions, CTR, positon) in Google Search Console. 12 Months recommended. Upload Queries.csv from the zip file.</li>
<li>Top 16 Positions Displayed (~2 SERP pages)</a>
</ol>
""", unsafe_allow_html=True)

get_gsc_file = st.file_uploader("Upload GSC CSV File",type=['csv']) 

if get_gsc_file is not None:
    st.write("Data upload success, processing... :sunglasses:")
    df = pd.read_csv(get_gsc_file)

    x = 1
    d = {'Position': [], 'Sum Clicks': [], 'Sum Impressions':[], 'Avg CTR':[],'Min CTR':[],'Max CTR':[],'Max CTR KW':[]}
    df2 = pd.DataFrame(data=d)

    while x < 17:
      df1 = df[(df['Position'] >=x) & (df['Position'] < x+1)]
      df1 = df1.sort_values('CTR',ascending=False)
      df1['CTR'] = df1['CTR'].str.replace('%','')
      df1['CTR'] = df1['CTR'].astype(np.float16)

      try:
        ctr = int(df1['CTR'].mean())
        ctr_min = int(df1['CTR'].min())
        ctr_max = int(df1['CTR'].max())
        ctr_max_kw = df1.iloc[0]['Top queries']

        clicks = int(df1['Clicks'].sum())
        impressions = int(df1['Impressions'].sum())
        data = {'Position': int((x)),'Sum Clicks':clicks,'Sum Impressions':impressions,'Avg CTR':ctr,'Min CTR':ctr_min,'Max CTR':ctr_max,'Max CTR KW':ctr_max_kw}
        print(data)
        df2 = df2.append(data, ignore_index=True)
        df2['Position'] = df2['Position'].astype(int)
        df2['Sum Clicks'] = df2['Sum Clicks'].astype(int)
        df2['Sum Impressions'] = df2['Sum Impressions'].astype(int)
        df2['Avg CTR'] = df2['Avg CTR'].astype(int)
        df2['Min CTR'] = df2['Min CTR'].astype(int)
        df2['Max CTR'] = df2['Max CTR'].astype(int)
        
        df2['Avg CTR'] = df2['Avg CTR'].astype(str)
        df2['Min CTR'] = df2['Min CTR'].astype(str)
        df2['Max CTR'] = df2['Max CTR'].astype(str)
        
        df2['Avg CTR'] = df2['Avg CTR'] + "%"
        df2['Min CTR'] = df2['Min CTR'] + "%"
        df2['Max CTR'] = df2['Max CTR'] + "%"
      except:
        pass
      x += 1
 
    def get_csv_download_link(df, title):
      csv = df.to_csv(index=False)
      b64 = base64.b64encode(csv.encode()).decode()
      return f'<a href="data:file/csv;base64,{b64}" download="{title}">Download CSV File</a>'
 
    st.markdown(get_csv_download_link(df2,"gsc-keyword-trends.csv"), unsafe_allow_html=True)
    st.dataframe(df2)
    st.write('Author: [Greg Bernhardt](https://twitter.com/GregBernhardt4) | Friends: [importSEM](https://www.importsem.com) and [Physics Forums](https://www.physicsforums.com)')
