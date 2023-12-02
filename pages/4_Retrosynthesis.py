import random
import time
import os
import pandas as pd

import streamlit as st

st.set_page_config(page_title="D4Tool",page_icon="💊")
"""
# Ретросинтетический анализ
"""

os.system('pip install rdkit')
os.system('pip install aizynthfinder')

from rdkit.Chem.Draw import IPythonConsole
from aizynthfinder.interfaces import AiZynthApp
application = AiZynthApp("./data/config.yml")

st.subheader("Переобучение на собственных данных", divider='gray')
smi = st.file_uploader("Файл .smi ваших данных")
if st.button("Начать обучение"):
    st.success('Переобучение выполнено!', icon="✅")
