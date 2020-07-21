import pandas as pd

df = pd.read_csv("../data/1-replaced.csv")

# Sum all the -1, 0, 1 to score the treaty
df["score"] = df.sum(axis=1, numeric_only=True)

# Rearrange columns
cols = ['score'] + [col for col in df if col != 'score']
df = df[cols]

# Check if it seems ok
print(df.head())
print(df['score'].describe())

# Export to csv
df.to_csv('../data/2-scored.csv', index=False)
print('Done.')