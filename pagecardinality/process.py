import pandas as pd
import pagecardinality.param


class process(object):


    def __init__(self, df):
        self.df = df
        self.results = {}
        self.__process_rows()


    def __process_rows(self):
        # loop through each row in the dataframe and process
        for row in self.df.itertuples():
            # split the rows

            if '?' in row.pagePath:
                stem,params = row.pagePath.split('?',1)
                p_array = self.__extract_params(params)
                # store the individual parameter in the global results
                for p in p_array.values():
                    p.related_urls = set([stem])
                    if p.param in self.results.keys():
                        self.results[p.param].merge(p)
                    else:
                        self.results[p.param] = p

    def __extract_params(self,str):
        params = {}

        pairs = str.split('&')
        for i in pairs:
            tmp = i.split('=',1)
            if len(tmp)==2:
                key=tmp[0]
                val=tmp[1]
            elif len(tmp)==1:
                key = tmp[0]
                val=''
            else:
                key = i
                val=''
            # create a new param object and set the attributes
            p = pagecardinality.param(key,val)
            params[key] = p

        # get the related parameters from this query string

        if len(params.keys())>1:
            # create a set of keys
            all_params = set([params[id].param for id in params.keys()])
            for p in params.keys():
                # get the difference between the individual parameter and the total set
                params[p].related_params = all_params.difference(set([p]))

        return params