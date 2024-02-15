from openai import OpenAI
import json
import pandas as pd
from pandas import json_normalize
import streamlit as st
import os
from io import BytesIO

st.header("Competitor Analysis")
# col1, col2 = st.columns(2)
# with col1:
#   file_name = st.text_input("Output File Name ","d:\dept\competitor_analysis")
# with col2:

fields_req = st.text_input("Required columns (comma separated)","Company name, Head quarter, Established Yr, No. of Employees,Company Turnover INR in Million, Market share, Market segment, Strength, Weakness,Latest info ")

with st.sidebar:
  Company_name= st.text_input("Organisation","TVS Sensing Solutions")
  no_of_companies=st.number_input("Top n companies",5,10)
  other_companies=st.text_input("Companies you want to include (comma separated)")

  inp_mkt = st.radio("",["Indian market","Global market"],horizontal = True)
  inp_mkt_sgement= st.selectbox("Market segment",("Automotive","Industrial Solutions"))
  inp_prd_segment = st.selectbox("Product Segment",("Switches", "Sensors", "Solenoids","ECC","Electro Mechanical assembly","IoT","Others") )
  inp_sub_segment=""
  if inp_prd_segment == "Sensors":
      inp_sub_segment= st.selectbox("Sub Segment",("Pressure Sensors","Temperature Sensors","Position Sensors","Level Sensors","Flow Sensors","Speed Sensors","Proximity Sensors","Acceleration Sensors","Force Sensors","Torque Sensors","Vibration Sensors","Gas Sensors","Humidity Sensors","Light Sensors","Image Sensors","Others"))
  elif inp_prd_segment=="Switches":
    inp_sub_segment= st.selectbox("Sub Segment",("Snap Action Switches","D3 switches","DB switches","Hood latch","Tactile Switches","Push Button Switches","Rocker Switches","Toggle Switches","Slide Switches","Limit Switches","Proximity Switches","Rotary Switches","DIP Switches","Reed Switches","Key Lock Switches","Micro Switches","Power Switches","Waterproof Switches","Others"))
  elif inp_prd_segment=="Solenoids":
    inp_sub_segment= st.selectbox("Sub Segment",("Cold Advance Solenoid","ESO solenoid","Fuel injector","AHI","Others"))
 
  prd_input= inp_sub_segment +" in "+inp_prd_segment



  if inp_prd_segment =="Others" or  inp_sub_segment == "Others":
      if inp_prd_segment == "Others":
        inp_sub_segment=""
      inp_sub_segment1 = st.text_input("Others")
      if inp_prd_segment !="Others":
        prd_input=inp_sub_segment1 +" in "+ inp_prd_segment
        
  inp_technology = st.text_input("Technology")
  if inp_technology != "":
      prd_input= prd_input+ " using "+inp_technology+" technology"
if inp_mkt=="Indian Market":
  inp_mkt1 = "Indian"
else :
   inp_mkt1="Global"
o_c = ""
if other_companies:
  o_c = ". excluding the top" + str(no_of_companies) + "companies, include these companies as well "+other_companies
usr_input= "List down top "+str(no_of_companies)+"  "+ inp_mkt1 +" companies manufacturing  "+prd_input+" similar to "+Company_name+" product in "+inp_mkt_sgement+" segment for "+ inp_mkt+" in json format without header inside the json and do not include contents other than json. All the numbers in the json data should be in string format such that they are inside double quotes" +" Required fields "+fields_req+o_c

but_status = st.button("Process")

def dataframe_to_excel(df):
    # Write Excel file to BytesIO object
    excel_data = BytesIO()
    with pd.ExcelWriter(excel_data, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False)
    excel_data.seek(0)
    return excel_data

if but_status:
    API_KEY = os.getenv('API_KEY')
  with st.spinner('Processing...'):
    client = OpenAI(api_key = API_KEY)
    context = "I am an industrial expert in automotive component manufacturing industry. I am doing automotive market research in "+inp_mkt
    completion = client.chat.completions.create(
      model="gpt-4",
      messages=[
          {"role": "user", "content": '{"context": "' + context + '", "format": "json"}'},
          {"role": "user", "content": usr_input}
      ]
    )
    
  obj = completion.choices[0].message.content
  json_in = str(obj)
  lis = json.loads(json_in)
  nobj = lis
  if len(lis) == 1:
      for i in lis:
          nobj = lis[i]
  json_in = json_in.replace("'", '"')
  df = json_normalize(lis)
  excel_data = dataframe_to_excel(df)
  st.download_button(label='Download Excel', data=excel_data, file_name='data.xlsx', mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
