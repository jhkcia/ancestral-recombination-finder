
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

def add_haplos(result_dict, path):
    print(f'Parsing file {path}')
    with open(path, encoding='utf-8') as f:
        for l in f.readlines():
            j = eval(l)
            result_dict[j[0]] = j[1]

def get_all_haplo_input_files():
    root_dir = './result/'
    result = []
    for x in os.listdir(root_dir):
        if x.endswith(".txt") and x.startswith('from'):
            result.append(root_dir+x)
    return result

def read_result(input_file=None):
    result ={}
    if input_file==None:
        for path in get_all_haplo_input_files():
            add_haplos(result ,path)
    else:
        add_haplos(result, input_file)

    return result

def generate_full_spans(result):
    spans = []
    
    for x in result.keys():
        for part in result[x]:
            spans.append([x, part[0], part[1]])

    return spans


def read_spans(input_file=None):
    result = read_result(input_file)
    spans = generate_full_spans(result)
    return spans