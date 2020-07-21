import pandas as pd

df = pd.read_csv("../data/0-data_cleaned.csv")

# Delete id column, it's automatically added by pandas so we don't need it
del df['id']

# Columns with 'Yes' = -1
special_cols = [
            "criteria/Scope and Definitions/Definition of investor/Specifying natural persons covered/Includes permanent residents",
            "criteria/Scope and Definitions/Definition of investor/Specifying natural persons covered/Excludes dual nationals",
            "criteria/Standards of Treatment/National treatment (NT)/Reference to ""like circumstances"" (or similar)",
            "criteria/Standards of Treatment/Prohibition on unreasonable, arbitrary or discriminatory measures",
            "criteria/Standards of Treatment/Protection from strife/Specifications/Absolute right to compensation in certain circumstances",
            "criteria/Standards of Treatment/Umbrella clause",
            "criteria/Standards of Treatment/Entry and sojourn of personnel (subject to local laws)",
            "criteria/Standards of Treatment/Senior management (nationality)",
            "criteria/Other Clauses/Transparency/Directed at States (obligation to publish laws and regulations)",
            "criteria/Other Clauses/Non-derogation clause (in case of IIA’s conflict with other norms, more favourable rules apply to investors)",
            "criteria/Other Clauses/Investment promotion/Reference to specific promotion activities in text of agreement (not preamble)",
            "criteria/Investor-State Dispute Settlement (ISDS)/ISDS included",
            "criteria/Investor-State Dispute Settlement (ISDS)/Forums/ISDS forum options/Domestic courts of the host State",
            "criteria/Investor-State Dispute Settlement (ISDS)/Forums/ISDS forum options/ICSID",
            "criteria/Investor-State Dispute Settlement (ISDS)/Forums/ISDS forum options/UNCITRAL",
            "criteria/Investor-State Dispute Settlement (ISDS)/Forums/ISDS forum options/Other forums",
            "criteria/Investor-State Dispute Settlement (ISDS)/Other specific ISDS features/Provisional measures",
            "criteria/Investor-State Dispute Settlement (ISDS)/Other specific ISDS features/Consolidation of claims"
            ]
data_columns = list(df.columns)

# Replace 'Yes' and 'No' values with corresponding -1, 0, 1
for col in data_columns:
    if col in special_cols:
        df[col].replace(to_replace = ['Yes', 'No'], value = [-1, 0], inplace=True)
    else:
        df[col].replace(to_replace = ['Yes', 'No'], value = [1, 0], inplace=True)

# Export to csv
df.to_csv('../data/1-replaced.csv', index=False)
print('Done.')
