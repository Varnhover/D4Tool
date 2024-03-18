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

# D4Tool

D4Tool is a novel online platform for searching new drug structures and molecular docking.\n
Generation of similar molecules, determination of toxicity, synthetic availability and molecular docking are performed using pre-trained neural networks.\n
This site is a demo-version of a user-friendly GUI, to use the full functionality of the programme use Google Colaboratory notepad instead.\n
Project code is available on GitHub.\n

* Generation of molecules according to a given structure
* Prediction of toxicity and synthetic availability of molecules
* Molecular docking\n

"""

st.image('mol.png')
