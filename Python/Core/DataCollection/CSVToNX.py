#Elliot Fisk: convert CSV edgelist format to networkx
import networkx as nx
import pandas as pd
import numpy as np

class CSVToNX:
    def __init__(self, filename):
        self.fn = filename

    def getNX(self):
        #net_df = pd.read_csv(self.fn, dtypes={'P1':object, 'P2':object, 'Count':'Int32'}, header=0, index_col=False)
        net_df = pd.read_csv(self.fn, names=['P1', 'P2'], dtype=object, header=0, index_col=False)
        print(net_df)
        net_df = net_df[(net_df['P1'] == 'tu-ra-am-i3-li2') | (net_df['P1'] == 'SI-A-a') | (net_df['P2'] == 'tu-ra-am-i3-li2') | (net_df['P2'] == 'SI-A-a')]
        print(net_df)
        #net_df = net_df[net_df['Count'] >= 2]
        gt = nx.Graph()
        G = nx.from_pandas_edgelist(net_df, source='P1', target='P2', create_using=gt)
        return G