import multiprocessing
from SNPDataSet import get_snp_dfs
from utils import convert_mutation_df_to_vcf
from SpanFinderNew import SpanFinder
import Constants


def find_for_items(maxRemovePercent, minSnpCount, start=None, end=None, fileName=None):
    muts = get_snp_dfs(minSnpCount, fileName)
    vcf = convert_mutation_df_to_vcf(muts)

    sf = SpanFinder(vcf, False)
    if start == None or end == None:
        start = 0
        end = len(muts['position'].unique())

    XX = sf.find_all_spans(maxRemovePercent, start, end)

    with open(f'./result/from{start}_to{end}.txt', 'w') as f:
        for item in XX:
            f.write("%s\n" % item)


if __name__ == "__main__":

    muts = get_snp_dfs(Constants.min_threshold)

    l = len(muts['position'].unique())
    # l = 10
    # threads = 4
    threads = 1
    siz = int(l/threads)+1
    processes = []
    for i in range(threads):
        start = i*siz
        end = (i+1)*siz
        print(f'from {start} to {end}')
        p = multiprocessing.Process(target=find_for_items, args=(
            Constants.MAX_THRESHOLD, Constants.min_threshold, start, end, ))
        processes.append(p)

    for p in processes:
        p.start()

    for p in processes:
        p.join()
