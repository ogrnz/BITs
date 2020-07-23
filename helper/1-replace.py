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
            "criteria/Investor-State Dispute Settlement (ISDS)/Other specific ISDS features/Consolidation of claims",
            "criteria.Preamble.Reference.to.social.investment.aspects..e.g..human.rights..labour..health..CSR..poverty.reduction"
            ]
data_columns = list(df.columns)

# Replace 'Yes' and 'No' values with corresponding -1, 0, 1
for col in data_columns:
    if col in special_cols:
        df[col].replace(to_replace = ['Yes', 'No'], value = [-1, 0], inplace=True)
    # cols with special replacement values
    elif col == 'criteria/Scope and Definitions/Temporal scope of the treaty/Investments covered':
        df[col].replace(to_replace = ['Applies to post-BIT investments only', "Applies to both pre-existing and post-BIT investments",'Not stipulated'], value = [1, -1, 0], inplace=True)
    elif col == 'criteria/Scope and Definitions/Temporal scope of the treaty/Disputes covered':
        df[col].replace(to_replace = ['Carves out pre-existing disputes', 'Not stipulated'], value = [1, 0], inplace=True)
    elif col == 'criteria/Standards of Treatment/National treatment (NT)/Type of NT clause':
        df[col].replace(to_replace = ['Post-establishment', 'Pre-establishment only', 'Pre- and post-establishment', 'None', 'Inconclusive'], value = [1, 1, -1, 0, 0], inplace=True)
    elif col == 'criteria/Standards of Treatment/Most-favoured-nation (MFN) treatment/Type of MFN clause':
        df[col].replace(to_replace = ['Post-establishment', 'Pre-establishment only', 'Pre- and post-establishment', 'None'], value = [1, 1, -1, 0], inplace=True)
    elif col == 'criteria/Standards of Treatment/Fair and equitable treatment (FET)/Type of FET clause':
        df[col].replace(to_replace = ['FET unqualified', 'FET qualified', 'None'], value = [1, -1, 0], inplace=True)
    elif col == 'criteria/Standards of Treatment/Fair and equitable treatment (FET)/FET qualified/By reference to international law':
        df[col].replace(to_replace = ['International law / principles of international law', 'Customary international law (CIL)', 'None'], value = [1, 1, 0], inplace=True)
    elif col == 'criteria/Standards of Treatment/Full protection and security':
        df[col].replace(to_replace = ['With reference to domestic law', 'Standard', 'No clause'], value = [1, -1, 0], inplace=True)
    elif col == 'criteria/Standards of Treatment/Expropriation/Scope of measures covered':
        df[col].replace(to_replace = ['Indirect expropriation not mentioned', 'Indirect expropriation mentioned', 'No expropriation clause'], value = [0, -1, 1], inplace=True)
    elif col == 'criteria/Standards of Treatment/Protection from strife/Specifications/Relative right to compensation (comparator)':
        df[col].replace(to_replace = ['MFN only', 'NT only', 'MFN and NT', 'None'], value = [-1, -1, -1, 0], inplace=True)
    elif col == 'criteria/Standards of Treatment/Prohibition of performance requirements (PRs)/Includes prohibition of PRs':
        df[col].replace(to_replace = ['Explicit PR clause', 'No explicit PR clause'], value = [-1, 0], inplace=True)
    elif col == 'criteria/Standards of Treatment/Prohibition of performance requirements (PRs)/Type of PR clause':
        df[col].replace(to_replace = ['TRIMS reference', 'List of prohibited PRs'], value = [-1, -1], inplace=True)
    elif col == 'criteria/Exceptions/Scheduling and reservations (in treaty texts and annexes)':
        df[col].replace(to_replace = ['Positive-list commitments', 'Negative-list reservations', 'Both positive list commitments and negative list reservations', 'None'], value = [1, 1, 1, 0], inplace=True)
    elif col == 'criteria/Investor-State Dispute Settlement (ISDS)/Alternatives to arbitration':
        df[col].replace(to_replace = ['Voluntary ADR (conciliation / mediation)', 'Compulsory ADR (conciliation / mediation)', 'None'], value = [0, 1, 0], inplace=True)
    elif col == 'criteria/Investor-State Dispute Settlement (ISDS)/Scope and consent/Scope of claims: general approach (chapeau paragraph of ISDS clause)':
        df[col].replace(to_replace = ['Covers any dispute relating to investment', 'Lists specific bases of claim beyond treaty (e.g. contractual disputes)', 'Covers treaty claims only', 'Other'], value = [-1, -1, -1, 0], inplace=True)
    elif col == 'criteria/Investor-State Dispute Settlement (ISDS)/Forums/Relationship between forums':
        df[col].replace(to_replace = ['No reference', '"Fork in the road"', '"No U turn" (waiver clause)', 'Preserving right to arbitration after domestic court proceedings', 'Local remedies first'], value = [0, 1, 1, -1, 1], inplace=True)
    elif col == 'criteria/Treaty Duration, Amendment and Termination/Treaty duration/Years of initial treaty term':
        df[col].replace(to_replace = ['5 years', '10 years', '15 years', '20 years', 'Other'], value = [1, -1, -1, -1, 0], inplace=True)
    elif col == 'criteria/Treaty Duration, Amendment and Termination/Automatic renewal':
        df[col].replace(to_replace = ['None', 'Indefinite term', '2 years', '5 years', '10 years', '15 years', '20 years', 'Other'], value = [0, -1, 1, 1, -1, -1, -1, 0], inplace=True)
    elif col == 'criteria/Treaty Duration, Amendment and Termination/Amendment and termination/"Survival"/"sunset" clause length':
        df[col].replace(to_replace = ['None', '5 years', '10 years', '15 years', '20 years', 'Other'], value = [0, 1, 1, -1, -1, 0], inplace=True)
    else:
        df[col].replace(to_replace = ['Yes', 'No'], value = [1, 0], inplace=True)

# Export to csv
df.to_csv('../data/1-replaced.csv', index=False)
print('Done.')
