import pandas as pd
import pagecardinality.param


class process(object):


    def __init__(self, df):
        self.df = df
        self.results = {}
        self.__process_rows()


    def __process_rows(self):
        # loop through each row in the dataframe and process
        for index,row in self.df.iterrows():
            # split the rows
            stem,params = row['pagePath'].split('?',1)
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
            key,val = i.split('=',1)
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