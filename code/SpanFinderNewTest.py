import pandas as pd
from SpanFinderNew import SpanFinder
from utils import convert_mutation_df_to_vcf

# print dataframe.
df
DF = convert_mutation_df_to_vcf(df)
sf = SpanFinder(DF, ['A', 'B', 'C', 'D', 'E', 'F', 'G'])
# X = sf.find_combinations(1, 3)

# Y = sf.find_spans(1,20)
# Y

# Z = sf.find_all_spans(0)
# assert Z == [[1, []], [3, []], [6, []], [7, [[8, []]]], [8, []]]

# Z = sf.find_all_spans(20)
# print(Z)
# assert Z ==[[1, [[3, {'G'}]]],
#  [3, [[6, {'C'}], [7, []], [8, []]]],
#  [6, [[7, {'B'}], [8, []]]],
#  [7, [[8, []]]],
#  [8, []]]

Z = sf.find_all_spans(40, 100)
print(Z)
assert Z ==[[1, [[3, {'G'}]]],
 [3, [[6, {'C'}], [7, []], [8, []]]],
 [6, [[7, {'B'}], [8, []]]],
 [7, [[8, []]]],
 [8, []]]

# Z = sf.find_all_spans(100)
# assert Z==[[1, [[3, {'G'}], [6, {'D', 'E'}], [7, {'B'}], [8, []]]],
#  [3, [[6, {'C'}], [7, []], [8, []]]],
#  [6, [[7, {'B'}], [8, []]]],
#  [7, [[8, []]]],
#  [8, []]]