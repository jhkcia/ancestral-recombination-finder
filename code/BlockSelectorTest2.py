from BlockSelector import BlockSelector

haplos = [
    [0, 100, 10],
    [100, 120, 10],
    [0, 40, 1],
    [40, 80, 1],
    [80, 120, 1],
    [0, 58, 2],
    # [2, 3, 0],
    # [3, 4, 1]
]

bs = BlockSelector(haplos, 20)
bs.find_best_match(2000)
result = bs.get_best_match_haplos()

print(result)
