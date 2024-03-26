import streamlit as st
import os
import joblib
import pandas
import sklearn #==0.23.2

st.set_page_config(page_title="D4Tool",page_icon="💊")
"""
# Toxicity and synthetic availability prediction
"""

smi = st.file_uploader("Your molecules .smi file")
def save_uploaded_file(uploadedfile):
  with open(os.path.join("dbs",uploadedfile.name),"wb") as f:
     f.write(uploadedfile.getbuffer())
  return st.success("Saved file :{} in dbs".format(uploadedfile.name))
save_uploaded_file(smi)

#f = open('results.smi', 'w')
#f.write("1")

#-- browser.gatherUsageStats false

if st.button("Start prediction"):
    if smi is None:
        smi = "test.smi"
    os.system(f'python ToxPred/etoxpred_predict.py --datafile dbs/.name --modelfile dbs/etoxpred_best_model.joblib --outputfile results.csv')
    st.write(pandas.read_csv('results.csv'))

st.subheader("Retrain model with your data", divider='gray')
train = st.file_uploader("Your data .smi file")
if st.button("Start retraining"):
    st.success('Retraining done!', icon="✅")
