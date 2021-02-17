from elasticsearch import Elasticsearch
import elasticsearch_dsl
from pprint import pprint as pp
import os
import pandas as pd
import xx_sent_ud_sm

import urllib.request
import urllib.parse
import json
import xml.etree.ElementTree as ET
import en_core_sci_lg
from collections import Counter
import os
import create_tokens as ct

# Variante 1
topicFile = "C:/Users/Fabian/Desktop/elastic/cord-metadata_qrels_topics/topics-rnd5_covid-complete.xml"
run = "best"
# %%
root = ET.parse(topicFile).getroot()
client = Elasticsearch([{'host': 'localhost'}, {'port': 9200}])


# %%


with open(path + run + '.txt', 'w') as f:
    for i, topic in enumerate(root.findall('topic')):
        # print(i)
        query = topic.find('query').text.lower()
        question = topic.find('question').text.lower()
        narrative = topic.find('narrative').text.lower()

        topic_id = topic.attrib.get('number')
        query_tokenized = tokenize_string(query)
        question_tokenized = tokenize_string(question)
        narrative_tokenized = tokenize_string(narrative)

        query_constructed = query_tokenized + " " + question_tokenized + " " + narrative_tokenized
        # print(len(query_constructed))
        # query_constructed = remove_dup(query_constructed.split())
        # print(len(query_constructed))
        # print("----------------")

        # search = client.search({
        #     "query": {
        #         "query_string": {
        #             "query": query_tokenized,
        #             "fields": ["title_token", "abstract_token"],
        #             "offsets": True,
        #             "payloads": True,
        #             "positions": True,
        #             "term_statistics": True,
        #             "field_statistics": True
        #
        #         }
        #     }
        # }, index="cord_tokenz", size="1050")

        search = client.search(
            {
                "query": {
                    "multi_match": {
                        "query": query_constructed,
                        "fields": ["title_token^1.5", "abstract_token"],
                        "type": "cross_fields",
                        "tie_breaker": 0.30,
                        "analyzer": "my_analyzer"
                    }
                },

            }, index="cord_tokenz", size="1050")

        dup_list = []
        counter = 0
        for i, hit in enumerate(search['hits'].get('hits'), 1):
            id = hit['_source'].get('cord_uid')
            if id not in dup_list and counter < 1000:
                counter += 1
                line = " ".join(
                    [str(topic_id), "0", str(hit['_source'].get('cord_uid')), str(counter), str(hit.get('_score')),
                     str(run), str('\n')])
                f.write(line)

            dup_list.append(id)
        # if len(set(ids)) < len(ids):
        #     i = [id_ for id_ in ids if ids.count(id_) > 1]
        #     print(topic_id,  i)

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
        "similarity":
            {
                "my_similarity": {
                    "type": "DFR",
                    "basic_model": "g",
                    "after_effect": "b",
                    "normalization": "z"
                }
            },
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
    index="livivo",
    body=body_index,
    ignore=400  # ignore 400 already exists code
)

# print out the response:
print('response:', response)
