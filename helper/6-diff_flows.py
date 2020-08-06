import pandas as pd
import numpy as np

df = pd.read_csv('../data/5-added_variables.csv')

for index, row in df.iterrows():
    #Difference of flows per Party = out + in
    outflowsP1 = df.loc[index, 'FDIOutflowsP1']
    inflowsP1 = df.loc[index, 'FDIInflowsP1']
    outflowsP2 = df.loc[index, 'FDIOutflowsP2']
    inflowsP2 = df.loc[index, 'FDIInflowsP2']

    df.loc[index, 'DiffFlowsP1'] = np.round(outflowsP1 + inflowsP1, decimals=4)
    df.loc[index, 'DiffFlowsP2'] = np.round(outflowsP2 + inflowsP2, decimals=4)
    '''
    if outflowsP1 > inflowsP1:
        df.loc[index, 'DiffFlowsP1'] = outflowsP1 - inflowsP1
    elif inflowsP1 > outflowsP1:
        df.loc[index, 'DiffFlowsP1'] = inflowsP1 - outflowsP1
    elif outflowsP2 > outflowsP2:
        df.loc[index, 'DiffFlowsP2'] = outflowsP2 - inflowsP2
    elif inflowsP2 > outflowsP2:
        df.loc[index, 'DiffFlowsP2'] = inflowsP2 - inflowsP2
    '''
    # Difference of total flows
    diff_p1 = df.loc[index, 'DiffFlowsP1']
    diff_p2 = df.loc[index, 'DiffFlowsP2']

    df.loc[index, 'DiffFlowsTot'] = np.round(np.absolute(diff_p1 - diff_p2), decimals=4)

# Rearrange columns order
cols_to_order = [
                'score', 'DiffFlowsTot',
                'DiffFlowsP1', 'DiffFlowsP2',
                'FDIOutflowsP1', 'FDIInflowsP1',
                'FDIOutflowsP2', 'FDIInflowsP2',
                'Party1', 'Party2', 'ISO-Party1', 'ISO-Party2',
                'Year of signature','name', 'Parties'
                ]
new_columns = cols_to_order + (df.columns.drop(cols_to_order).tolist())
df = df[new_columns]

# Export to csv
df.to_csv('../data/6-diff_flows.csv', index=False)
print('Done.')
