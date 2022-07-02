
import numpy as np
import pandas as pd
import gzip


def get_vcf_names(vcf_path):
    with open(vcf_path) as ifile:
          for line in ifile:
            if line.startswith("#CHROM"):
                  vcf_names = [x for x in line.split('\t')]
                  break
    ifile.close()
    return vcf_names

 


def get_row_array(row, samples):
    arr= []
    for s in samples:
        phased = row[s].split('|')
        arr.append(int(phased[0]))
        arr.append(int(phased[1]))
    return arr

def create_mutations_df(vcf, samples, min_threshold):
    all_items = []
    for i, row in vcf.iterrows():
        arr = get_row_array(row, samples)
        items = []
        for s in range(len(samples)):
            val1 = arr[2*s]
            val2 = arr[2*s+1]
            if(val1!=0):
                items.append([row['POS'], f'{samples[s]}_0', val1 ])
            if val2 !=0:
                items.append([row['POS'], f'{samples[s]}_1', val2 ])
        if len(items)>min_threshold:
            all_items.extend(items)
    df = pd.DataFrame(all_items, columns = ['position', 'sample', 'state'])
    return df

FILE_NAME = '../simulation.vcf'

def get_snp_dfs(min_threshold):
    names = get_vcf_names(FILE_NAME)
    names
    # vcf = pd.read_csv(FILE_NAME, comment='#', chunksize=1000000, delim_whitespace=True, header=None, names=names)
    vcf = pd.read_csv(FILE_NAME, comment='#', nrows=10000,skiprows=0, delim_whitespace=True, header=None, names=names)


    samples = names[9:]

    mutations_df = create_mutations_df(vcf, samples, min_threshold)
    
    return mutations_df

def get_test_mutation_df():
    data = [
    ['A', 1, 1],
    ['A', 6, 1],
    ['A', 8, 1],
    ['B', 1, 1],
    ['B', 7, 1],
    ['B', 8, 1],
    ['C', 1, 1],
    ['C', 3, 1],
    ['C', 6, 1],
    ['C', 7, 1],
    ['C', 8, 1],
    ['D', 1, 1],
    ['D', 3, 1],
    ['D', 8, 1],
    ['E', 6, 1],
    ['E', 8, 1],
    ['F', 8, 1],
    ['G', 3, 1],
    ['G', 8, 1]
    ]
    
    # Create the pandas DataFrame
    return pd.DataFrame(data, columns = ['sample', 'position', 'state'])
    