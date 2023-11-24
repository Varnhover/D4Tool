import streamlit as st
import pandas as pd
import os
import joblib
import pandas
import sklearn #==0.23.2

st.set_page_config(page_title="D4Tool",page_icon="💊")
"""
# Молекулярный докинг
"""


#@title PDB + SMILES input

print('Please, enter PDB protein id.')
PDB_id = st.text_input('Введите PDB id вашего лиганда') #1GOS
print('Please, enter SMILES of the docking molecule.')
SMILES_or_pubchem_id = st.text_input('Введите SMILES молекулы') #CCOC(=O)C1=CCN(C)CC1

print('Download a tar file containing all results?(y/n)')
dwnld = st.checkbox('Скачать tar файл с результатами?')
if dwnld:
  download_results = True
else:
  download_results = False
st.button("Начать Докинг")

import os
import requests
import time
from random import random

#os.system('pip install torch')

def download_pdb_file(pdb_id: str) -> str:
    """Download pdb file as a string from rcsb.org"""
    PDB_DIR ="/tmp/pdb/"
    os.makedirs(PDB_DIR, exist_ok=True)

    if pdb_id.startswith('http'):
        url = pdb_id
        filename = url.split('/')[-1]
    elif pdb_id.endswith(".pdb"):
        return pdb_id
    else:
        if pdb_id.startswith("AF"):
            url = f"https://alphafold.ebi.ac.uk/files/{pdb_id}-model_v3.pdb"
        else:
            url = f"http://files.rcsb.org/view/{pdb_id}.pdb"
        filename = f'{pdb_id}.pdb'

    cache_path = os.path.join(PDB_DIR, filename)
    if os.path.exists(cache_path):
        return cache_path

    pdb_req = requests.get(url)
    pdb_req.raise_for_status()
    open(cache_path, 'w').write(pdb_req.text)
    return cache_path

def download_smiles_str(pubchem_id: str, retries:int = 2) -> str:
    """Given a pubchem id, get a smiles string"""
    while True:
        req = requests.get(f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/CID/{pubchem_id}/property/CanonicalSMILES/CSV")
        smiles_url_csv = req.text if req.status_code == 200 else None
        if smiles_url_csv is not None:
            break
        if retries == 0:
            return None
        time.sleep(1+random())
        retries -= 1

    return smiles_url_csv.splitlines()[1].split(',')[1].strip('"').strip("'") if smiles_url_csv is not None else None

if not PDB_id or not SMILES_or_pubchem_id:
    PDB_id = "6agt"
    SMILES_or_pubchem_id = "COc(cc1)ccc1C#N"
    print(f"No input supplied. Using example data: {PDB_id} and {SMILES_or_pubchem_id}")

pdb_files = [download_pdb_file(_PDB_id) for _PDB_id in PDB_id.split(",")]
smiless = [download_smiles_str(_SMILES_or_pubchem_id) if str(_SMILES_or_pubchem_id).isnumeric() else _SMILES_or_pubchem_id
           for _SMILES_or_pubchem_id in SMILES_or_pubchem_id.split(',') ]

with open("/tmp/input_protein_ligand.csv", 'w') as out:
    out.write("protein_path,ligand\n")
    for pdb_file in pdb_files:
        for smiles in smiless:
            out.write(f"{pdb_file},{smiles}\n")


os.system('rm -rf /D4Tool/DiffDock/results')



os.system('pip install ipython-autotime --quiet')

if not os.path.exists("/D4Tool/DiffDock"):
#     %cd /D4Tool
    os.system('git clone https://github.com/gcorso/DiffDock.git')
#     %cd /D4Tool/DiffDock
    os.system('git checkout a6c5275')

try:
    import biopandas
except:
    os.system('pip install pyg==0.7.1 --quiet')
    os.system('pip install pyyaml==6.0 --quiet')
    os.system('pip install scipy==1.7.3 --quiet')
    os.system('pip install networkx==2.6.3 --quiet')
    os.system('pip install biopython==1.79 --quiet')
    os.system('pip install rdkit-pypi==2022.03.5 --quiet')
    os.system('pip install e3nn==0.5.0 --quiet')
    os.system('pip install spyrmsd==0.5.2 --quiet')
    os.system('pip install pandas==1.5.3 --quiet')
    os.system('pip install biopandas==0.4.1 --quiet')

import torch
print(torch.__version__)

try:
    import torch_geometric
except ModuleNotFoundError:
    os.system('pip uninstall torch-scatter torch-sparse torch-geometric torch-cluster  --y')
    os.system('pip install torch-scatter -f https://data.pyg.org/whl/torch-{torch.__version__}.html --quiet')
    os.system('pip install torch-sparse -f https://data.pyg.org/whl/torch-{torch.__version__}.html --quiet')
    os.system('pip install torch-cluster -f https://data.pyg.org/whl/torch-{torch.__version__}.html --quiet')
    os.system('pip install git+https://github.com/pyg-team/pytorch_geometric.git  --quiet')


##if not os.path.exists("/D4Tool/DiffDock/esm"):
###     %cd /D4Tool/DiffDock
##    os.system('git clone https://github.com/facebookresearch/esm')
###     %cd /D4Tool/DiffDock/esm
##    os.system('git checkout ca8a710') # remove/update for more up to date code
##    os.system('sudo pip install -e .')
###     %cd /D4Tool/DiffDock

os.system('git clone https://github.com/facebookresearch/esm')
os.system('git checkout ca8a710') # remove/update for more up to date code
os.system('sudo pip install -e .')

# %cd /D4Tool/DiffDock
os.system('python datasets/esm_embedding_preparation.py --protein_ligand_csv /tmp/input_protein_ligand.csv --out_file data/prepared_for_esm.fasta')

# %cd /D4Tool/DiffDock
# %env HOME=esm/model_weights
# %env PYTHONPATH=$PYTHONPATH:/D4Tool/DiffDock/esm
os.system('python /D4Tool/DiffDock/esm/scripts/extract.py esm2_t33_650M_UR50D data/prepared_for_esm.fasta data/esm2_output --repr_layers 33 --include per_tok --truncation_seq_length 30000')

# %cd /D4Tool/DiffDock
os.system('python -m inference --protein_ligand_csv /tmp/input_protein_ligand.csv --out_dir results/user_predictions_small --inference_steps 20 --samples_per_complex 40 --batch_size 6')

# %cd /D4Tool/DiffDock
os.system('wget https://sourceforge.net/projects/smina/files/smina.static/download -O smina && chmod +x smina')
os.system('wget https://github.com/gnina/gnina/releases/download/v1.0.3/gnina -O gnina && chmod +x gnina')

import re
import pandas as pd
from glob import glob
from shlex import quote
from datetime import datetime
from tqdm.auto import tqdm

# %cd /D4Tool/DiffDock/results/user_predictions_small
results_dirs = glob("./index*")

rows = []
for results_dir in tqdm(results_dirs, desc="runs"):
    results_pdb_file = "/tmp/pdb/" + re.findall("tmp-pdb-(.+\.pdb)", results_dir)[0]
    results_smiles = re.findall("pdb_+(.+)", results_dir)[0]
    results_sdfs = [os.path.join(results_dir, f) for f in os.listdir(results_dir) if "confidence" in f and f.endswith(".sdf")]

    results_pdb_file_no_hetatms = f"{results_pdb_file}_nohet.pdb"
    os.system('grep -v "^HETATM" {results_pdb_file} > {results_pdb_file_no_hetatms}')
    os.system('cp {results_pdb_file} .')

    for results_sdf in tqdm(results_sdfs, leave=False, desc="files"):
        confidence = re.findall("confidence([\-\.\d]+)\.sdf", results_sdf)[0]

        scored_stdout = os.system('/D4Tool/DiffDock/gnina --score_only -r "{results_pdb_file_no_hetatms}" -l "{results_sdf}"')
        scored_affinity = re.findall("Affinity:\s*([\-\.\d+]+)", '\n'.join(scored_stdout))[0]
        minimized_stdout = os.system('/D4Tool/DiffDock/gnina --local_only --minimize -r "{results_pdb_file_no_hetatms}" -l "{results_sdf}" --autobox_ligand "{results_sdf}" --autobox_add 2')
        minimized_affinity = re.findall("Affinity:\s*([\-\.\d+]+)", '\n'.join(minimized_stdout))[0]

        rows.append((results_pdb_file.split('/')[-1], results_smiles, float(confidence), float(scored_affinity), float(minimized_affinity), results_sdf))

df_results = pd.DataFrame(rows, columns=["pdb_file", "smiles", "diffdock_confidence", "gnina_scored_affinity", "gnina_minimized_affinity", "sdf_file"])
df_results_tsv = "df_diffdock_results.tsv"
df_results.to_csv(df_results_tsv, sep='\t', index=None)

out_pdbs = ' '.join(set(df_results.pdb_file.apply(quote)))
out_sdfs = ' '.join(df_results.sdf_file.apply(quote))

if download_results:
    tarname = f"diffdock_{datetime.now().isoformat()[2:10].replace('-','')}"
    _ = os.system("tar cvf {tarname}.tar --transform 's,^,{tarname}/,' --transform 's,\./,,' {out_pdbs} {out_sdfs} {df_results_tsv}")

    files.download(f"{tarname}.tar")


import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import linregress
# %config InlineBackend.figure_format='retina'

for (pdb_file, smiles), df_group in df_results.groupby(["pdb_file", "smiles"]):
    f, ax = plt.subplots(1, 2, figsize=(20,8))
    sns.regplot(data=df_group, x="diffdock_confidence", y="gnina_scored_affinity", ax=ax[0]);
    sns.regplot(data=df_group, x="diffdock_confidence", y="gnina_minimized_affinity", ax=ax[1]);

    slope, intercept, r_value_scored, p_value, std_err = linregress(df_group["diffdock_confidence"], df_group["gnina_scored_affinity"])
    slope, intercept, r_value_minimized, p_value, std_err = linregress(df_group["diffdock_confidence"], df_group["gnina_minimized_affinity"])
    ax[0].set_title(f"{pdb_file} {smiles[:30]} gnina scored r={r_value_scored:.3f}");
    ax[1].set_title(f"{pdb_file} {smiles[:30]} gnina minimized r={r_value_minimized:.3f}");

df_results.sort_values("diffdock_confidence", ascending=False).head(3)


os.system('pip install py3dmol==2.0.3 --quiet')

from IPython.display import HTML
import py3Dmol

resid_hover = """
function(atom,viewer) {
    if(!atom.label) {
        atom.label = viewer.addLabel(atom.chain+" "+atom.resn+" "+atom.resi,
            {position: atom, backgroundColor: 'mintcream', fontColor:'black', fontSize:12});
    }
}"""
unhover_func = """
function(atom,viewer) {
    if(atom.label) {
        viewer.removeLabel(atom.label);
        delete atom.label;
    }
}"""

view = py3Dmol.view(width=800, height=800)
view.setCameraParameters({'fov': 35, 'z': 100});


top_hit = df_results.sort_values("diffdock_confidence", ascending=False).iloc[0]
print("top hit:")
display(top_hit)

view.addModel(open(top_hit.sdf_file).read(), "sdf")
view.setStyle({"model": 0}, {'stick':{"color":"#ff0000"}})
view.setViewStyle({"model": 0}, {'style':'outline','color':'black','width':0.1})
view.zoomTo();

view.addModel(open(top_hit.pdb_file).read(), "pdb");
view.setStyle({"model": 1}, {"cartoon":{"color":"spectrum"}})
view.setStyle({"model": 1, "hetflag":True}, {'stick':{"color":"spectrum"}})

model = view.getModel()
model.setHoverable({}, True, resid_hover, unhover_func)

view
