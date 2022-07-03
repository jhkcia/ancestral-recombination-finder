import multiprocessing
from utils import read_spans, get_all_haplo_input_files
from TimeFinder import TimeFinder
from SNPDataSet import get_snp_dfs
import Constants


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


def infer_times(path, min_threshold, vcf_path):
    spans = read_spans(path)
    mutation_df = get_snp_dfs(min_threshold, vcf_path)

    population = [p for p in mutation_df['sample'].unique()]
    muts = [p for p in mutation_df['position'].unique()]

    #vcf  --from-bp 48055079 --to-bp 48085036
    start = min(muts) - 100  # 48055079
    end = max(muts)+100  # 48085036
    if start < 0:
        start = 0

    centers = find_centers(muts, start, end)
    mosaics = []
    for s in spans:
        S, E = find_span_mosaic(centers, s[0], s[1])
        mosaics.append([S, E, s[2]])
    tf = TimeFinder(mosaics, population, mutation_df)

    times = tf.find_all_times()
    file_name = f"infer_time_{path.split('/')[-1]}"
    with open(f'./result/{file_name}', 'w') as f:
        f.write("%s\n" % times)
    return tf

if __name__ == "__main__":
    dirs = get_all_haplo_input_files()
    processes = []
    for d in dirs:
        p = multiprocessing.Process(target=infer_times, args=(
            d, Constants.min_threshold, Constants.vcf_path))
        processes.append(p)

    for p in processes:
        p.start()

    for p in processes:
        p.join()
