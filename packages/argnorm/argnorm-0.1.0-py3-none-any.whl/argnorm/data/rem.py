import pandas as pd
from glob import glob
ts = glob('*.tsv')

for t in ts:
    p = pd.read_table(t, index_col=0)
    if p.columns[0] != 'Original ID':
        continue
    p.query('`Original ID` == "vanXmurFvanKWI_1_NZAGAF01000127"')
    p.query('`Original ID` == "sitABCD_1_AY598030"')
    p.query('`Original ID` == "qacC_1_M37889"')
    p['Original ID'].value_counts()

    if p['ARO'].dtype.kind == 'f':
        p['ARO'] = p.ARO.map(lambda x: ('' if pd.isnull(x) else str(int(x))))
    p.to_csv('renamed/'+t, sep='\t', index=False)

# Read the data

