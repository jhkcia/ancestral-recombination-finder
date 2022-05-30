
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


import os
def read_result():
    root_dir = './result/'
    result ={}
    for x in os.listdir(root_dir):
        if x.endswith(".txt") and x.startswith('from'):
            # Prints only text file present in My Folder
            print(f'Parsing file {x}')
            with open(root_dir+x, encoding='utf-8') as f:
                for l in f.readlines():
                    j = eval(l)
                    result[j[0]] = j[1]
    return result

# def generate_spans(result):
#     spans = []
    
#     for x in result.keys():
#         for part in result[x]:
#             spans.append([x, part[0], len(part[1])])

#     return spans

def generate_full_spans(result):
    spans = []
    
    for x in result.keys():
        for part in result[x]:
            spans.append([x, part[0], part[1]])

    return spans


def read_spans():
    result = read_result()
    spans = generate_full_spans(result)
    return spans