from utils import read_spans, get_all_haplo_input_files
from TimeFinder import TimeFinder
from SNPDataSet import get_snp_dfs


def find_centers(mutations, start, end):
    M = sorted(mutations)
    R = [start]
    for i in range(len(M)-1):
        R.append((M[i]+M[i+1])/2)
    R.append(end)
    return R


def find_span_mosaic(centers, start, end):
    S = None
    E = None
    for pos in centers:
        if pos < start:
            S = pos
        elif pos > end:
            E = pos
            break
    return S, E

def infer_times(path):
    spans = read_spans(path)
    mutation_df = get_snp_dfs()

    population = [p for p in mutation_df['sample'].unique()]
    muts = [p for p in mutation_df['position'].unique()]
    
    #vcf  --from-bp 48055079 --to-bp 48085036 
    
    centers = find_centers(muts, 48055079, 48085036 )
    mosaics = []
    for s in spans:
        S, E = find_span_mosaic(centers, s[0], s[1])
        mosaics.append([S, E, s[2]])
    tf = TimeFinder(mosaics, population, mutation_df)

    times = tf.find_all_times()
    file_name = f"infer_time_{path.split('/')[-1]}"
    with open(f'./result/{file_name}', 'w') as f:
        f.write("%s\n" % times)

import multiprocessing

if __name__ == "__main__":

    dirs = get_all_haplo_input_files()
    processes = []
    for d in dirs:
        p = multiprocessing.Process(target=infer_times, args=(d, ))
        processes.append(p)

    for p in processes:
        p.start()

    for p in processes:
        p.join()
