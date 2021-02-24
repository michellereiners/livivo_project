from elasticsearch import Elasticsearch
from pprint import pprint as pp
import pandas as pd
import numpy as np
import xx_sent_ud_sm
import re

import en_core_sci_lg
from collections import Counter
import os
import tokens_functions as tf
#%%
from pprint import pprint as pp
# Variante 1
topicFile = "C:/Users/Fabian/Desktop/elastic/cord-metadata_qrels_topics/topics-rnd5_covid-complete.xml"
run = "third_run"
# %%
root = pd.read_json("C:/Users/Fabian/PycharmProjects/Livivo/data/livivo/candidates/livivo_hq_1000.jsonl", lines=True)
client = Elasticsearch([{'host': 'localhost'}, {'port': 9200}])

path = "C:/Users/Fabian/PycharmProjects/Livivo/git/livivo_project/"


#%%


d = tf.tokenize_string_uni("sars")
#%%
df = pd.DataFrame(columns=['qid', 'query', 'new_query', 'cnt_results', 'relevant_found'])


p = 0


with open(path + run + '.txt', 'w') as f:
    for i_topic in range(len(root)):
        # print(p)
        p += 1
        query = root.iloc[i_topic, 1]

        topic_id = root.iloc[i_topic, 0]
        operator = 'or'
        if ' AND ' in query and not ' OR ' in query:
            operator = 'and'


        query_tokenized_uni = tf.tokenize_string_uni(query)
        query_tokenized_sci = tf.tokenize_string_sci(query)



        search = client.search(body={
                "query": {
                    "bool": {
                        "should":[ {
                            "query_string": {
                                "query": query_tokenized_sci,
                                "default_operator": operator,
                                "fields": ["MESH_TOKENZ^10", "CHEM_TOKENZ^10"],
                                "analyzer": "comma"
                            }
                        },
                            {
                                "query_string": {
                                    "query": query_tokenized_uni,
                                    "default_operator": operator,
                                    "fields": ["TITLE_TOKENZ", "ABSTRACT_TOKENZ"],
                                    "analyzer": "comma"

                            }}
                        ]
                    }
                }

            }, index="livivo", size="100")

        counter = 0

        result_len = len(search['hits'].get('hits'))

        candidates_query = candidates[candidates['qid'] == topic_id]['candidates'].values[0]
        relevant_found = []
        for result in search['hits'].get('hits'):
            result_id = result['_source'].get('DBRECORDID')
            if result_id in candidates_query:
                relevant_found.append(result_id)

        relevant_found = list(set(relevant_found))



        df = df.append({'qid': topic_id, 'query': query, 'new_query': query_tokenized_uni,
                        'cnt_results': result_len,
                        'relevant_found': len(relevant_found)}, ignore_index=True)
        if result_len > 0:
            for i, hit in enumerate(search['hits'].get('hits'), 1):
                id = hit['_source'].get('qid')

                line = " ".join(
                    [str(topic_id), "0", str(hit['_source'].get('DBRECORDID')), str(counter), str(hit.get('_score')),
                     str(run), str('\n')])
                f.write(line)
                counter += 1
#%%
df['cnt_results'].replace(0, np.nan, inplace=True)
df['cnt_results'].fillna(1, inplace=True)
df['share'] = df['relevant_found'] / df['cnt_results']
df.sort_values(by='share', ascending=False, inplace=True)
df.reset_index(inplace=True, drop=True)
# if len(set(ids)) < len(ids):
#     i = [id_ for id_ in ids if ids.count(id_) > 1]
#     print(topic_id,  i)

#%%

df.to_csv("result_evaluation.csv", index=False)
# %%
from elasticsearch import Elasticsearch
import elasticsearch_dsl
from pprint import pprint as pp
import os
import urllib.request
import urllib.parse
import json
import xml.etree.ElementTree as ET


# %%

root = ET.parse(topicFile).getroot()
client = Elasticsearch([{'host': 'localhost'}, {'port': 9200}])

os.chdir("C:/Users/Fabian/PycharmProjects/Livivo")

# %%
body_index = {
    "settings": {
        # "similarity":
        #     {
        #         "my_similarity": {
        #             "type": "DFR",
        #             "basic_model": "g",
        #             "after_effect": "b",
        #             "normalization": "z"
        #         }
        #     },
        "analysis": {
            "tokenizer": {
                "comma": {
                    "type": "pattern",
                    "pattern": ","
                }
            },
            "analyzer": {
                "comma": {
                    "type": "custom",
                    "tokenizer": "comma"
                },
                "whitespace": {
                    "type": "custom",
                    "tokenizer": "whitespace"
                }
            }
        }
    },
    "mappings": {
        "properties": {
            "CBRECORDID": {
                "type": "text",
                "index": False,
            },
            "LANGUAGE": {
                "type": "text",
                "index": False
            },
            "MESH_TOKENZ": {
                "type": "text",
                "index": True,
                "analyzer": "comma",
                "similarity": "my_similarity"

            },
            "CHEM_TOKENZ": {
                "type": "text",
                "index": True,
                "analyzer": "comma",
                "similarity": "my_similarity"

            },
            "TITLE_TOKENZ":  {
                "type": "text",
                "index": True,
                "analyzer": "whitespace",
                "similarity": "my_similarity"
            },
            "ABSTRACT_TOKENZ":  {
                "type": "text",
                "index": True,
                "analyzer": "whitespace",
                "similarity": "my_similarity"
            }
        }
    }
}

# make an API call to the Elasticsearch cluster
# and have it return a response:
response = client.indices.create(
    index="livivo_bm25",
    body=body_index,
    ignore=400  # ignore 400 already exists code
)

# print out the response:
print('response:', response)
