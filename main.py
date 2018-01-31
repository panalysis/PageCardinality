import pagecardinality as pc
from google2pandas import *
import pandas as pd
import os.path
import operator

cachename = 'tmp.pkl'
my_id = '1232xxxx'

def get_gadata(id,fname):
    query = {\
        'ids'             : id,
        'metrics'         : 'pageviews',
        'dimensions'      : 'pagePath',
        'filters'         : 'pagePath=~\?',
        'start_date'      : '30daysAgo',
        'sort'            : '-pageviews',
        'max_results'     : 10000}

    ga = GoogleAnalyticsQuery(token_file_name='analytics.dat')
    pages_df, metadata = ga.execute_query(all_results=True, **query)
    pages_df.to_pickle(fname)
    return pages_df

def get_pickle(f):
    return pd.read_pickle(f)

def get_data(id,fname):
    if os.path.isfile(fname):
        return get_pickle(fname)
    else:
        return get_gadata(id, fname)

if __name__ == '__main__':

    sample = True
    sample_size = 10000

    df = get_data(my_id,cachename);
    population = df.shape[0]

    if sample:
        df = df.sample(sample_size).copy()

    ppr = pc.process(df)

    res = []
    for p in (sorted(ppr.results.values(), key=operator.methodcaller('calculate_permutations'), reverse=True)):
        res.append(p.get_data())

    res_df = pd.DataFrame(res)
    res_df.to_excel("results.xlsx", index=False)