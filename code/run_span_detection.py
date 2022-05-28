from SNPDataSet import get_snp_dfs
from utils import convert_mutation_df_to_vcf
from SpanFinderNew import SpanFinder


MAX_THRESHOLD = 30
def find_for_items(start, end):
    muts = get_snp_dfs()
    vcf = convert_mutation_df_to_vcf(muts)

    sf = SpanFinder(vcf, False)

    XX = sf.find_all_spans(MAX_THRESHOLD, start, end)

    with open(f'./result/from{start}_to{end}.txt', 'w') as f:
        for item in XX:
            f.write("%s\n" % item)




import multiprocessing


if __name__ == "__main__":

    muts = get_snp_dfs()

    l = len(muts['position'].unique())
    # l = 10
    # threads = 4
    threads = 20
    siz = int(l/threads)+1
    processes = []
    for i in range (threads):
        start = i*siz
        end = (i+1)*siz
        print(f'from {start} to {end}')
        p = multiprocessing.Process(target=find_for_items, args=(start,end, ))
        processes.append(p)

    for p in processes:
        p.start()

    for p in processes:
        p.join()
