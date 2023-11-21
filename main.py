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

D4Tool - первая в РФ онлайн-платформа для поиска новых структур лекарств и молекулярного докинга.\n
Генерация схожих молекул, определение токсичности, синтетической доступности и молекулярный докинг осуществляются с помощью предобученных нейронных сетей.\n
Данный сайт предстовляет собой демо-версию удобного GUI, для использования полного функционала программы используйте блокнот Google Colaboratory.\n
Весь код проекта доступен по репозитории GitHub D4Tool/.\n

* Генерация молекул по заданной структуре
* Прогноз токсичности и синтетической доступности молекул
* Молекулярный докинг\n

"""

st.image('mol.png')