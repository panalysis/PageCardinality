__author__ = 'rodj'

import math
import operator

class param(object):

    def __init__(self, p, v):
        self.param = p
        self.values = {
            v : self.param_value(v)
        }
        self.rows = 1
        self.related_params = set()
        self.related_urls = set()


    def merge(self,p):
        # method to ensure that existing values are updated as each row is processed
        for v in p.values.keys():
            if v in self.values.keys():
                self.values[v].count +=1
            else:
                self.values[v] = p.values[v]
        self.rows += 1
        self.related_params = self.related_params.union(p.related_params)
        self.related_urls = self.related_urls.union(p.related_urls)

    def calculate_permutations(self):
        res = len(self.related_urls) * math.factorial(len(self.related_params)) * len(self.values.keys())
        # as factorial combinations can be huge set the maximum number to the largest 32 bit unsigned integer
        if res>2147483647:
            res=2147483647
        return res

    def get_data(self):
        vals = sorted(self.values.values(), key=operator.attrgetter('count'), reverse=True)
        vlist = []
        for v in vals:
            vlist.append(v.value)

        if len(vlist)>5:
            vlist = vlist[0:4]

        return {
            'param'                : self.param,
            'max_cardinality'      : self.calculate_permutations(),
            'rows'                 : self.rows,
            'related_params'       : list(self.related_params),
            'related_urls'         : list(self.related_urls),
            'num_values'           : len(vals),
            'values'               : vlist
        }

    def __str__(self):
        return "Param: "  + self.param + " Max Permutations: " + str(self.calculate_permutations()) + " Rows: " + str(self.rows) ;


    # nested class to create an object that can be used within a dictionary to get a count of each value
    class param_value(object):
        def __init__(self, v):
            self.value = v
            self.count = 1

        def __str__(self):
            return self.value