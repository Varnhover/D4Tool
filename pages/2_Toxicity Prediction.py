import streamlit as st
import pandas as pd
import os
import joblib
import pandas
import sklearn #==0.23.2

st.set_page_config(page_title="D4Tool",page_icon="💊")
"""
# Определение токсичности и синтетической доступности
"""

st.file_uploader("Файл .csv ваших молекул")
st.button("Предсказать токсичность")

#f = open('results.csv', 'w')
#f.write("1")

#-- browser.gatherUsageStats false
if st.button:
    os.system('streamlit run https://github.com/Varnhover/D4Tool/blob/main/ToxPred/etoxpred_predict.py')
    #os.system('git clone https://github.com/Varnhover/D4Tool')
    #os.system('python D4Tool/ToxPred/etoxpred_predict.py --datafile test.smi --modelfile dbs/etoxpred_best_model.joblib --outputfile results.csv')
    #st.write(pd.read_csv('ToxPred/results(Rasagiline).csv'))
