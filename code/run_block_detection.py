
from utils import read_result_spans

spans = read_result_spans()

from BlockSelector import BlockSelector

for m in range(4000, 7000, 50):
    bs = BlockSelector(spans, 2504*2)
    bs.find_best_match(m)

    result = bs.get_best_match_haplos()
    stats = bs.get_statistics()
    print(stats)
    with open(f'./result/hotspots_{m}.txt', 'w') as f:
        f.write("%s\n" % result)