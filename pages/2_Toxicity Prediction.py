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


import argparse

import pandas as pd

from rdkit import Chem
from rdkit import rdBase
from rdkit.Chem import AllChem

import numpy as np

from sascore import SAscore
from joblib import load

rdBase.DisableLog('rdApp.error')

def myargs():
    parser = argparse.ArgumentParser()                                              
    parser.add_argument('--datafile', required=True, 
                        help='training data filename')
    parser.add_argument('--modelfile', required=True,
                        help='path to the model to load')
    parser.add_argument('--outputfile', required=False, default='./results.csv',
                        help='output file to save the result')
    args = parser.parse_args()
    return args

def load_data(filename):
    """
    Loading data from .smi file. And generating Morgan's fingerprints and labels 
    for the smiles data.
    Input: filename -> path to the .smi file in the format of SmilesString\tCompoundName\tLabel
    Output: two arrays X -> fingerprints, y -> labels
    """
    df = pd.read_csv(filename, sep='\t', names=['smiles', 'name'])
    smiles_list = df['smiles'].tolist()
    mols = [Chem.MolFromSmiles(x) for x in smiles_list]
    names = df['name'].tolist()
    X = []
    cnt = 0
    for mol in mols:
        if mol is None:
            print('Error encountered parsing SMILES {}'.format(smiles_list[cnt]))
            continue
        mol = Chem.AddHs(mol)
        fp = AllChem.GetMorganFingerprintAsBitVect(mol, radius=2, nBits=1024)
        fp_string = fp.ToBitString()
        tmpX = np.array(list(fp_string),dtype=float)
        X.append(tmpX)
        cnt += 1
    X = np.array(X)
    return X, smiles_list, names

def predict(opt):
    df = pd.DataFrame(columns=['name', 'smiles', 'Tox-score', 'SAscore'])
    # laod the data
    X, smiles_list, names = load_data(opt.datafile)
    # load the saved model and make predictions
    print('...loading models')
    clf = load(opt.modelfile)
    reg = SAscore()
    print('...starts prediction')
    for i in range(X.shape[0]):
        tox_score = clf.predict_proba(X[i,:].reshape((1,1024)))[:,1]
        sa_score = reg(smiles_list[i])
        df.at[i, 'name'] = names[i]
        df.at[i, 'smiles'] = smiles_list[i]
        df.at[i, 'Tox-score'] = tox_score[0]
        df.at[i, 'SAscore'] = sa_score
    print('...prediction done!')
    df.to_csv(opt.outputfile, index=False)

if st.button:
    #os.system('streamlit run https://github.com/Varnhover/D4Tool/blob/main/ToxPred/etoxpred_predict.py')
    #os.system('git clone https://github.com/Varnhover/D4Tool')
    #os.system('pip install joblib')
    #os.system('pip install sklearn')
    #os.system('python D4Tool/ToxPred/etoxpred_predict.py --datafile test.smi --modelfile dbs/etoxpred_best_model.joblib --outputfile results.csv')
    #st.write(pd.read_csv('ToxPred/results(Rasagiline).csv'))
    opt = myargs()
    predict(opt)
