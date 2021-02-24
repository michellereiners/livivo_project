import pandas as pd



candidates = pd.read_json(path_or_buf="data/livivo/candidates/livivo_hq_100_candidates.jsonl", lines=True)

#%%

def get_l(x):
    return len(set(x))


candidates['cnt'] = candidates['candidates'].apply(get_l)
#%%
candidates.sort_values(by='cnt', ascending=False, inplace=True)
#%%
f = candidates[['qid', 'cnt']]

f.reset_index(inplace=True, drop=True)
#%%

f.to_csv("cnt_candidates_pro_query.csv", index=False)