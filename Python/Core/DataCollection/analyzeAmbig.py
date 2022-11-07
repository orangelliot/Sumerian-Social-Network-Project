import pandas as pd

CULLING_SIZE = 1000

net_df = pd.read_csv(f'ambig_tablet_net{CULLING_SIZE}.csv', dtype='int')
net_df = net_df[net_df['shared_names'] > 0]

print(net_df.info())

net_df = net_df[((net_df['tab2_year'] >= 68) & (net_df['tab2_year'] <= 72)) | ((net_df['tab2_year'] >= 58) & (net_df['tab2_year'] <= 62))]
net_df = net_df[net_df['shared_names'] > 0]

#net_df.to_csv(f'ambig_tablet_net{CULLING_SIZE}_relevant.csv', header=True, mode='a', index=False)

print(net_df.groupby('tab1').tab2_year.mean())

#amar-sin 6 is ~70

#sulgi 42 is ~60