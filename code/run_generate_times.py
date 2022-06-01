from utils import read_spans, get_all_haplo_input_files
from TimeFinder import TimeFinder
from SNPDataSet import get_snp_dfs

def infer_times(path):
    spans = read_spans(path)
    mutation_df = get_snp_dfs()

    population = [p for p in mutation_df['sample'].unique()]
    tf = TimeFinder(spans, population, mutation_df)

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
