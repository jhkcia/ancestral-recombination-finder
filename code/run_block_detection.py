
from BlockSelector import BlockSelector
from utils import read_full_timed_mosaics
import Constants


spans = read_full_timed_mosaics(
    Constants.min_threshold, Constants.MAX_THRESHOLD, None)


for m in range(4000, 7000, 50):
    print(f'checking M= {m}')
    bs = BlockSelector(spans, 2504*2)
    bs.find_best_match(m)

    result = bs.get_best_match_haplos()
    stats = bs.get_statistics()
    print(stats)
    with open(f'./result/hotspots_{m}.txt', 'w') as f:
        f.write("%s\n" % result)
