import pandas as pd
# from elasticsearch import Elasticsearch
import xx_sent_ud_sm
import en_core_sci_lg
import os

# client = Elasticsearch([{'host': 'localhost'}, {'port': 9200}])

nlp_uni = xx_sent_ud_sm.load()
nlp_sci = en_core_sci_lg.load()


# UNIVERSAL
def is_token_allowed_uni(token):
    '''
         Only allow valid tokens which are not stop words
         and punctuation symbols.
    '''
    if not token or not token.text.strip() or token.is_stop or token.is_punct:
        return False
    return True


def preprocesstoken_uni(token):
    # Reduce token to its lowercase lemma form
    return token.lemma_.strip().lower()


def tokenize_uni(x):
    try:
        return str([preprocesstoken_uni(token) for token in nlp_uni(x) if is_token_allowed_uni(token)])
    except:
        return str([])


def tokenize_string_uni(x):
    return ",".join([preprocesstoken_uni(token) for token in nlp_sci(x) if is_token_allowed_uni(token)])


# SCIENTIFIC
def is_token_allowed_sci(token):
    '''
         Only allow valid tokens which are not stop words
         and punctuation symbols.
    '''
    if not token or not token.text.strip() or token.is_stop or token.is_punct:
        return False
    return True


def preprocesstoken_sci(token):
    # Reduce token to its lowercase lemma form
    return token.lemma_.strip().lower()


def tokenize_sci(x):
    try:
        return str([preprocesstoken_sci(token) for token in nlp_sci(x) if is_token_allowed_sci(token)])
    except:
        return str([])


def tokenize_string_sci(x):
    return ",".join([preprocesstoken_sci(token) for token in nlp_sci(x) if is_token_allowed_sci(token)])


def prettify(x):
    if type(x) == list:
        x = x[0]
    return x.replace("[", "").replace("]", "").lstrip("'").rstrip("'").lstrip('"').rstrip('"')


def prettify_v2(x):
    if type(x) == list:
        x = x[0]
    return x.replace("[", "").replace("]", "").replace("'", "").replace('"', "")



#%%

df = pd.read_csv("all_filtered_final.csv", delimiter=";")
print("Hello")
df.fillna(value="", inplace=True)


try:
    df['KEYWORDS_TOKENZ'] = df['KEYWORDS'].apply(tokenize_string_sci)
except:
    pass

df['TITLE_TOKENZ'] = df['TITLE'].apply(tokenize_string_uni)
print("tit_to")

df['ABSTRACT_TOKENZ'] = df['ABSTRACT'].apply(tokenize_string_uni)
print("ab_to")

df['MESH_TOKENZ'] = df['MESH'].apply(tokenize_string_sci)
print("mesh_to")

df['CHEM_TOKENZ'] = df['CHEM'].apply(tokenize_string_sci)
print("chem_to")


df.to_csv(f"tokenz.csv", index=False)
