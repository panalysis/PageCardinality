import pandas as pd
import re

df = pd.read_pickle('tmp.pkl')

params_remove = [
    'limitno',
    'q',
    'v',
    'c',
    'm',
    'a',
    'v',
    'w',
    'postcode',
    'responsive',
    'searchsuburb',
    'jinvid',
    'jassignid',
    'checksum',
    'style',
    'src_type',

]

def remove_params(url):
    rx = re.compile("(\W)(" + "|".join(params_remove) + ")=[^&$]+&?")
    res = rx.sub(r"\1",url)
    return res


df['tmp'] = df['pagePath'].apply(lambda x: remove_params(x))
df[['tmp','pageviews']].groupby('tmp').count().shape

df[['tmp','pageviews']].groupby('tmp').count().sort('pageviews',ascending=False).head(20)