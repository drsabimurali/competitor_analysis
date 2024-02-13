from openai import OpenAI
import json
import pandas as pd
from pandas import json_normalize
import streamlit as st
import os

st.header("Competitor Analysis")
col1, col2 = st.columns(2)
with col1:
  file_name = st.text_input("Output File Name ","d:\dept\competitor_analysis")
with col2:
  but_status = st.button("Process")

fields_req = st.text_input("Required output information","Company name, Head quarter, Established Yr, No. of Employees,Turnover INR, Market share, Market segment, Strength, Weakness,Latest info ")

with st.sidebar:
  Company_name= st.text_input("Organisation","TVS Sensing Solutions")
  no_of_companies= st.slider("Top n companies",5,25,step=5)
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

usr_input= "List down top "+str(no_of_companies)+" companies manufacturing  "+prd_input+" similar to "+Company_name+" product in "+inp_mkt_sgement+" segment for "+ inp_mkt+" in json format without header inside the json and do not include contents other than json. " +" Required fields "+fields_req 

st.write(usr_input)
st.markdown(
    f'<div style="background-color: lightblue; padding: 10px;">'
    f'<h2 style="color: black;>{usr_input}</h2>'
    '</div>',
    unsafe_allow_html=True
)

if but_status and file_name:
  API_KEY = os.getenv('API_KEY')
  client = OpenAI(api_key = API_KEY)
  context = "I am an industrial expert in automotive component manufacturing industry. I am doing automotive market research in "+inp_mkt
  completion = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "user", "content": '{"context": "' + context + '", "format": "json"}'},
        {"role": "user", "content": usr_input}
    ]
  )

  st.write(completion.choices[0].message.content)

  json_in = str(completion.choices[0].message.content)
  lis = json.loads(json_in)
  df = json_normalize(lis)
  excel_data = dataframe_to_excel(df)
  st.download_button(label='Download Excel', data=excel_data, file_name='data.xlsx', mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
