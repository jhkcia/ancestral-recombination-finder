
import numpy as np
import pandas as pd


def convert_mutation_df_to_vcf(df):
    positions = df['position'].unique()
    positions.sort()
    positions

    samples = df['sample'].unique()

    dtt = np.zeros([len(samples), len(positions)], dtype=int)
    vcf_df = pd.DataFrame(dtt, columns=positions, index=samples)
    for i, row in df.iterrows():
        if i%10000 == 0:
            print(f'{i}, {len(df)}')
        vcf_df[row.position][row['sample']] = 1     # first "column" then "row"
    return vcf_df
