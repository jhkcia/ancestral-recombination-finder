from BlockSelector import BlockSelector

haplos = [
    [0, 1, 1],
    [0, 2, 3],
    [0, 3, 5],
    [1, 2, 1],
    [1, 4, 3],
    [1, 3, 2],
    [2, 3, 0],
    [3, 4, 1]
]

bs = BlockSelector(haplos)
bs.find_best_match(0, 1)
result = bs.get_best_match_haplos()
print(result)
assert result == [0, 1, 4]