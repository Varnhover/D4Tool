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
from streamlit_ketcher import st_ketcher
IPythonConsole.molSize = (400,300)
IPythonConsole.ipython_useSVG=True

from crem.crem import mutate_mol

import streamlit as st
#from main import *

st.set_page_config(page_title="D4Tool",page_icon="💊")
"""
# Molecule generation from SMILES
"""
smiles = "CC(=O)O"
molecule = st.text_input("Please enter your molecule SMILES", "CCC(=O)OC")
smiles = st_ketcher(molecule)
n = st.slider('Please enter the contex radius', 1,20)

with zipfile.ZipFile('dbs/replacements02_sc2.zip', 'r') as zip_ref:
    zip_ref.extractall('dbs/')
db_fname = 'dbs/replacements02_sc2.db'

if st.button("Generate molecules"):
    #O=C(C)Oc1ccccc1C(=O)O
    mol = Chem.MolFromSmiles(smiles)
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
        st.image(rdkit.Chem.Draw.MolsToImage(mols))
    else:
        st.warning("No molecules were synthesised. Maybe you should try different context radius. If it doesn't help, your molecule probably lacks functional groups")

st.subheader("Retrain AI model on your data", divider='gray')
smidb = st.file_uploader("Your data .smi file")
if st.button("Start retrainig"):
    st.success('Retraining done!', icon="✅")
