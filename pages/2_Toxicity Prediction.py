import streamlit as st
import os
import joblib
import pandas
import sklearn #==0.23.2

st.set_page_config(page_title="D4Tool",page_icon="💊")
"""
# Определение токсичности и синтетической доступности
"""

csv = st.file_uploader("Файл .csv ваших молекул")


#f = open('results.csv', 'w')
#f.write("1")

#-- browser.gatherUsageStats false


if csv is None:
    csv = "test.smi"

if st.button("Предсказать токсичность"):
    os.system('pip install rdkit')
    os.system('pip install joblib')
    os.system('pip install scikit-learn==1.2.2')
    os.system('pip install pandas')
    os.system(f'python ToxPred/etoxpred_predict.py --datafile {csv} --modelfile dbs/etoxpred_best_model.joblib --outputfile results.csv')
    st.write(pandas.read_csv('results.csv'))

st.subheader("Переобучение на собственных данных", divider='gray')
smi = st.file_uploader("Файл .smi ваших данных")
if st.button("Начать обучение"):
    csv = csv
