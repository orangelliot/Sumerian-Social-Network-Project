#Elliot Fisk: convert CSV edgelist format to networkx
import networkx as nx
import pandas as pd
import numpy as np

class CSVToNX:
    def __init__(self, filename):
        self.fn = filename

    def getNX(self):
        net_df = pd.read_csv(self.fn, dtype={'P1':'S32', 'P2':'S32', 'Count':'Int64'})
        print(len(net_df))
        net_df = net_df[net_df['Count'] >= 5]
        #print(len(net_df))
        gt = nx.Graph()
        G = nx.from_pandas_edgelist(net_df, source='P1', target='P2', create_using=gt)
        return G