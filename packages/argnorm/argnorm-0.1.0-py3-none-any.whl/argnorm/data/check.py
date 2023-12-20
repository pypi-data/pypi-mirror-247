import pandas as pd
from glob import glob

tsvs = glob('*.tsv')

for t in tsvs:
    x = pd.read_table(t, index_col=0)
    alti = x[x.columns[0]]
    if len(set(alti)) != len(alti):
        print(t)

    alti
    len(alti)
    alti.value_counts().value_counts()
    x.query('`Original ID` == "qacC_1_M37889"')


            vanXmurFvanKWI_1_NZAGAF01000127"')
    x.head()
