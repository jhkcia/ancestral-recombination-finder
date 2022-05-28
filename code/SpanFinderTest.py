

from SpanFinder import SpanFinder
import pandas as pd

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
df = pd.DataFrame(data, columns = ['sample', 'position', 'state'])
  
# print dataframe.
df

sf = SpanFinder(df, ['A', 'B', 'C', 'D', 'E', 'F', 'G'])
# X = sf.find_combinations(1, 3)

# Y = sf.find_spans(1,20)
# Y

Z = sf.find_all_spans(0)
assert Z == [[1, []], [3, []], [6, []], [7, [[8, []]]], [8, []]]

Z = sf.find_all_spans(20)
assert Z ==[[1, [[3, {'G'}]]],
 [3, [[6, {'C'}], [7, []], [8, []]]],
 [6, [[7, {'B'}], [8, []]]],
 [7, [[8, []]]],
 [8, []]]

Z = sf.find_all_spans(40)
assert Z ==[[1, [[3, {'G'}]]],
 [3, [[6, {'C'}], [7, []], [8, []]]],
 [6, [[7, {'B'}], [8, []]]],
 [7, [[8, []]]],
 [8, []]]

Z = sf.find_all_spans(100)
assert Z==[[1, [[3, {'G'}], [6, {'D', 'E'}], [7, {'B'}], [8, []]]],
 [3, [[6, {'C'}], [7, []], [8, []]]],
 [6, [[7, {'B'}], [8, []]]],
 [7, [[8, []]]],
 [8, []]]