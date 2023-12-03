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
    st.write(f"The project ID is {rxn.project_id}")
    results = rxn4chemistry_wrapper.get_predict_automatic_retrosynthesis_results(
        response['prediction_id']
    )
    predict_automatic_retrosynthesis_response = rxn.predict_automatic_retrosynthesis(product=smiles)
    predict_automatic_retrosynthesis_results = rxn.get_predict_automatic_retrosynthesis_results(
        predict_automatic_retrosynthesis_response['prediction_id']
    )
    
    while predict_automatic_retrosynthesis_results['status'] != 'SUCCESS':
        predict_automatic_retrosynthesis_results = rxn.get_predict_automatic_retrosynthesis_results(
            predict_automatic_retrosynthesis_response['prediction_id']
        )
        time.sleep(30)

    def collect_reactions_from_retrosynthesis(tree: Dict) -> List[str]:
        reactions = []
        if 'children' in tree and len(tree['children']):
            reactions.append(
                AllChem.ReactionFromSmarts('{}>>{}'.format(
                    '.'.join([node['smiles'] for node in tree['children']]),
                    tree['smiles']
                ), useSmiles=True)
            )
        for node in tree['children']:
            reactions.extend(collect_reactions_from_retrosynthesis(node))
        return reactions
    for index, tree in enumerate(predict_automatic_retrosynthesis_results['retrosynthetic_paths']):
        print('Showing path {} with confidence {}:'.format(index, tree['confidence']))
        for reaction in collect_reactions_from_retrosynthesis(tree):
            display(Chem.Draw.ReactionToImage(reaction))
