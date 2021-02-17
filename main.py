import pandas as pd
import numpy as np
#%%
df = pd.read_json(path_or_buf="data/livivo/documents/livivo_medline_04.jsonl", lines=True, chunksize=100000)

#%%

base = pd.DataFrame()
i = 0
for x in df:
    print(i)
    i += 1
    base = base.append(x, ignore_index=True)
#%%

cand = pd.read_json(path_or_buf="data/livivo/candidates/livivo_hq_100_candidates.jsonl", lines=True, chunksize=100000)
#%%
cand_base = pd.DataFrame()
for x in cand:
    cand_base = cand_base.append(x, ignore_index=True)

#%%

rel_docs = cand_base.candidates.values

rel_docs_ids = []
for l in rel_docs:
    for x in l:
        rel_docs_ids.append(x)

rel_docs_ids = list(set(rel_docs_ids))
#%%

base_mod = base.loc[:,['DBRECORDID', 'TITLE', 'ABSTRACT', 'LANGUAGE', 'MESH', 'CHEM']]


base_filtered = base_mod[base_mod['DBRECORDID'].isin(rel_docs_ids)]




base_filtered.to_csv("data/livivo/documents/livivo_medline_04_filtered.csv", index=False)

#%%

all_csv = pd.DataFrame()
import os
for file in os.listdir("git/livivo_project/Data"):
    all_csv = all_csv.append(pd.read_csv(f"git/livivo_project/Data/{file}"), ignore_index=True)

#%%

all_csv.to_csv("git/livivo_project/Data/livivo_medline_all_filtered.csv", index=False)