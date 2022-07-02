
from SNPDataSet import get_snp_dfs
import os
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
        if i % 10000 == 0:
            print(f'{i}, {len(df)}')
        vcf_df[row.position][row['sample']] = 1     # first "column" then "row"
    return vcf_df


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
    result = {}
    if input_file == None:
        for path in get_all_haplo_input_files():
            add_haplos(result, path)
    else:
        add_haplos(result, input_file)

    return result


def generate_full_spans(result, add_single_point):
    spans = []

    for x in result.keys():
        if add_single_point:
            spans.append([x, x, []])
        for part in result[x]:
            spans.append([x, part[0], part[1]])

    return spans


def read_spans(input_file=None):
    result = read_result(input_file)
    spans = generate_full_spans(result, True)
    return spans


def read_full_spans(min_threshold, input_file=None):
    result = read_result(input_file)
    spans = generate_full_spans(result, True)

    muts = get_snp_dfs(min_threshold)
    positions = list(muts['position'].unique())
    spans_with_mut_count = []
    for s in spans:
        x = len([p for p in positions if p >= s[0] and p <= s[1]])
        spans_with_mut_count.append([s[0], s[1], s[2], x])

    # START | END | REMOVAL | MUT_COUNT
    return spans_with_mut_count


def get_timed_haplo_input_files():
    root_dir = './result/'
    result = []
    for x in os.listdir(root_dir):
        if x.endswith(".txt") and x.startswith('infer_time'):
            result.append(root_dir+x)
    return result


def add_timed_haplos(result_dict, path):
    print(f'Parsing file {path}')
    with open(path, encoding='utf-8') as f:
        for l in f.readlines():
            line = eval(l)
            for j in line:
                result_dict[f"{j[0]}_{j[1]}"] = j


def read_timed_result(input_file=None):
    result = {}
    if input_file == None:
        for path in get_timed_haplo_input_files():
            add_timed_haplos(result, path)
    else:
        add_timed_haplos(result, input_file)

    return result


def generate_timed_spans(result):
    spans = []

    for x in result.values():
        spans.append(x)

    return spans


def read_timed_mosaics(input_file=None):
    result = read_timed_result(input_file)
    spans = generate_timed_spans(result)
    return spans


def read_full_timed_mosaics(min_threshold, vcf_file,  input_file=None):
    spans = read_timed_mosaics(input_file)
    muts = get_snp_dfs(min_threshold, vcf_file)
    positions = list(muts['position'].unique())
    R = []
    for s in spans:
        x = len([p for p in positions if p >= s[0] and p <= s[1]])
        R.append([s[0], s[1], s[2], s[3], x])
    return R
