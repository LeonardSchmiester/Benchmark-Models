import pandas as pd

model = "Parmar_PCB2019"

f = model + "/" + "measurementData_" + model + ".tsv"
df = pd.read_csv(f, sep='\t')
for i, _ in df.iterrows():
    #df.iloc[i, 0] = df.iloc[i, 0][:-4]
    df.iloc[i, 0] = 'observable_' + df.iloc[i, 0]

df.to_csv(f, sep='\t', index=False)
