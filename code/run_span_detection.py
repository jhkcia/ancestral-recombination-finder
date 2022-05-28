from SNPDataSet import get_snp_dfs
from utils import convert_mutation_df_to_vcf
from SpanFinderNew import SpanFinder

muts = get_snp_dfs()
vcf = convert_mutation_df_to_vcf(muts)

sf = SpanFinder(vcf, False)

XX = sf.find_all_spans(10, -1)

with open('your_file.txt', 'w') as f:
    for item in XX:
        f.write("%s\n" % item)