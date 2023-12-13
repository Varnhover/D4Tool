import streamlit as st
import os
import joblib
import pandas
import sklearn #==0.23.2

st.set_page_config(page_title="D4Tool",page_icon="💊")
"""
# Toxicity and synthetic availability prediction
"""

csv = st.file_uploader("Your molecules .csv file")


#f = open('results.csv', 'w')
#f.write("1")

#-- browser.gatherUsageStats false


if csv is None:
    csv = "test.smi"

if st.button("Start prediction"):
    os.system('pip install rdkit')
    os.system('pip install joblib')
    os.system('pip install scikit-learn==1.2.2')
    os.system('pip install pandas')
    os.system(f'python ToxPred/etoxpred_predict.py --datafile {csv} --modelfile dbs/etoxpred_best_model.joblib --outputfile results.csv')
    st.write(pandas.read_csv('results.csv'))

st.subheader("Retrain model with your data", divider='gray')
smi = st.file_uploader("Your data .smi file")
if st.button("Start retraining"):
    st.success('Переобучение выполнено!', icon="✅")
