import random
import time
import os
import pandas as pd

import rdkit.Chem.Draw
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Draw
from rdkit.Chem.Draw import rdMolDraw2D
from rdkit.Chem.Draw import IPythonConsole
import zipfile
from IPython.display import SVG, Image
IPythonConsole.molSize = (400,300)
IPythonConsole.ipython_useSVG=True

from crem.crem import mutate_mol

import streamlit as st
#from main import *

st.set_page_config(page_title="D4Tool",page_icon="💊")
"""
# Генерация молекул по исходным SMILES
"""
smiles = "CC(=O)O"
smiles = st.text_input('Введите SMILES молекулы')
n = st.slider('Введите количество атомов, которые вы хотите поменять', 1,20)

with zipfile.ZipFile('dbs/replacements02_sc2.zip', 'r') as zip_ref:
    zip_ref.extractall('dbs/')
db_fname = 'dbs/replacements02_sc2.db'

if st.button("Начать генерацию"):
    #O=C(C)Oc1ccccc1C(=O)O
    mol = Chem.MolFromSmiles(smiles)
    img = rdkit.Chem.Draw.MolToImage(mol)
    #st.image(img)
    mols = list(mutate_mol(mol, db_fname, max_size=n))
    print(mols)
    string = ''
    for molecule in mols:
      string += str(molecule)
      string += '\n'
    file = open('test.smi', 'w')
    file.write(string)
    file.close()
    mols = list(mutate_mol(mol, db_fname, return_mol=True, max_size=n))
    mols = [Chem.RemoveHs(i[1]) for i in mols]
    if len(mols) != 0:
        #st.image(rdkit.Chem.Draw.MolsToImage(mols))
        st.image(rdkit.Chem.Draw.MolsToGridImage(mols[:8], molsPerRow=4, subImgSize=(300,200)))
    else:
        st.warning("No molecules were synthesised. Maybe you should try different context radius. If it doesn't help, your molecule probably lacks functional groups")

st.subheader("Переобучение на собственных данных", divider='gray')
smi = st.file_uploader("Файл .smi ваших данных")
if st.button("Начать обучение"):
    st.success('Переобучение выполнено!', icon="✅")
