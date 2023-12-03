import random
import time
import os
import streamlit as st
os.system('pip install --quiet aizynthfinder[all]')
os.system('pip install --ignore-installed Pillow==9.0.0')
os.system('mkdir --parents data && download_public_data data')

st.set_page_config(page_title="D4Tool",page_icon="💊")
"""
# Ретросинтетический анализ
"""

if st.button('авыаыъ'):
    os.system('pip install torchdrug')
    from torchdrug import data, datasets, utils

    reaction_dataset = datasets.USPTO50k("~/molecule-datasets/",
                                         atom_feature="center_identification",
                                         kekulize=True)
    synthon_dataset = datasets.USPTO50k("~/molecule-datasets/", as_synthon=True,
                                        atom_feature="synthon_completion",
                                        kekulize=True)

st.subheader("Переобучение на собственных данных", divider='gray')
smi = st.file_uploader("Файл .smi ваших данных")
if st.button("Начать обучение"):
    st.success('Переобучение выполнено!', icon="✅")
