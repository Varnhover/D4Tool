import streamlit as st
import pandas as pd
import os
import joblib
import sklearn #==0.23.2
import requests
import time
from random import random

st.set_page_config(page_title="D4Tool",page_icon="💊")
"""
# Molecular docking
"""


#@title PDB + SMILES input

PDB_id = st.text_input('Please, enter PDB protein id') #1GOS
SMILES_or_pubchem_id = st.text_input('Please, enter SMILES of the docking molecule.') #CCOC(=O)C1=CCN(C)CC1

dwnld = st.checkbox('Download a tar file containing all results?')
if dwnld:
  download_results = True
else:
  download_results = False
st.button("Start docking")
