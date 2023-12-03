import random
import time
import os
import streamlit as st
os.system('pip install rxn4chemistry')
from rxn4chemistry import RXN4ChemistryWrapper

st.set_page_config(page_title="D4Tool",page_icon="💊")
"""
# Ретросинтетический анализ
"""

smiles = "CC(=O)O"
smiles = st.text_input('Введите SMILES молекулы')
if st.button('авыаыъ'):
    api_key = "apk-35dc3d5d3a5d34065ff8f0c9cc90e8896aca7628400e8c5232f530ac7a612c7a3da4b4a0a37afdb6287126d41c7b8daddca846e6f73fc8ca566e558441aa651a8f340dff4970d7e82c734968506f6a04"
    rxn = RXN4ChemistryWrapper(api_key=api_key)

st.subheader("Переобучение на собственных данных", divider='gray')
smi = st.file_uploader("Файл .smi ваших данных")
if st.button("Начать обучение"):
    st.success('Переобучение выполнено!', icon="✅")
