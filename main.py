import pandas as pd
import os

cand = pd.read_json(path_or_buf="../../data/livivo/candidates/livivo_hq_100_candidates.jsonl", lines=True)


rel_docs = cand.candidates.values

rel_docs_ids = []
for l in rel_docs:
    for x in l:
        rel_docs_ids.append(x)

rel_docs_ids = list(set(rel_docs_ids))

no = ['10', '05', '04']
for file in os.listdir("../../data/livivo/documents"):
    if any([x in file for x in no]):
        continue
    print(file)
    df = pd.read_json(path_or_buf=f"../../data/livivo/documents/{file}", lines=True)
    print("Hello")
    cols = ['DBRECORDID', 'TITLE', 'ABSTRACT', 'LANGUAGE']

    if 'MESH' in df.columns:
        cols.append('MESH')
    if 'CHEM' in df.columns:
        cols.append('CHEM')
    if 'KEYWORDS' in df.columns:
        cols.append('KEYWORDS')

    base_mod = df.loc[:, cols]
    base_filtered = base_mod[base_mod['DBRECORDID'].isin(rel_docs_ids)]

    file_base_name = "".join(file.split(".")[:-1])
    base_filtered.to_csv(f"{file_base_name}_filtered.csv", index=False)
#%%
import pandas as pd
import os

df = pd.DataFrame()
for f in os.listdir("filtered_docs/"):
    df_local = pd.read_csv(f"filtered_docs/{f}")
    df = df.append(df_local)

df.to_csv("all_filtered.csv", index=False)


