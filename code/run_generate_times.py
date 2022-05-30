from utils import read_spans
from TimeFinder import TimeFinder

spans = read_spans()

from SNPDataSet import get_snp_dfs

mutation_df = get_snp_dfs()

population = [p for p in mutation_df['sample'].unique()]
tf = TimeFinder(spans, population, mutation_df)

times = tf.find_all_times()

with open(f'./result/haplo_times.txt', 'w') as f:
    f.write("%s\n" % times)