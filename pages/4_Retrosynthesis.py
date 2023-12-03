import random
import time
import os
import streamlit as st
os.system('pip install rxn4chemistry')
from rxn4chemistry import RXN4ChemistryWrapper
from typing import Dict, List
from IPython.display import display
from rdkit import Chem
from rdkit.Chem import AllChem

st.set_page_config(page_title="D4Tool",page_icon="💊")
"""
# Ретросинтетический анализ
"""

smiles = "CC(=O)O"
smiles = st.text_input('Введите SMILES молекулы')
if st.button('авыаыъ'):
    api_key = "apk-35dc3d5d3a5d34065ff8f0c9cc90e8896aca7628400e8c5232f530ac7a612c7a3da4b4a0a37afdb6287126d41c7b8daddca846e6f73fc8ca566e558441aa651a8f340dff4970d7e82c734968506f6a04"
    rxn = RXN4ChemistryWrapper(api_key=api_key)
    rxn.create_project("rxn-d4tool")
    rxn.set_project(rxn.project_id)
    time.sleep(5)
    response = rxn.predict_automatic_retrosynthesis(product=smiles)
    st.write("started...")
    time.sleep(5)
    results = rxn.get_predict_automatic_retrosynthesis_results(response['prediction_id'])
    time.sleep(5)

    while results['status'] != 'SUCCESS':
        results = rxn.get_predict_automatic_retrosynthesis_results(response['prediction_id'])
        st.write("checking retro...")
        time.sleep(15)
    st.write("success!")

    def collect_reactions(tree):
        reactions = []
        if 'children' in tree and len(tree['children']):
            reactions.append(
                AllChem.ReactionFromSmarts('{}>>{}'.format(
                    '.'.join([node['smiles'] for node in tree['children']]),
                    tree['smiles']
                ), useSmiles=True)
            )
        for node in tree['children']:
            reactions.extend(collect_reactions(node))
        return reactions

    #Display the suggested routes
    for index, path in enumerate(results['retrosynthetic_paths']):
        print('Showing path {} with confidence {}:'.format(index, path['confidence']))
        for reaction in collect_reactions(path):
            display(Chem.Draw.ReactionToImage(reaction))
