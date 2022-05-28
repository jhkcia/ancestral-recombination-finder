import os
def read_result():
    root_dir = './result/'
    result ={}
    for x in os.listdir(root_dir):
        if x.endswith(".txt") and x.startswith('from'):
            # Prints only text file present in My Folder
            print(f'Parsing file {x}')
            with open(root_dir+x, encoding='utf-8') as f:
                for l in f.readlines():
                    j = eval(l)
                    result[j[0]] = j[1]
    return result

def generate_spans(result):
    spans = []
    
    for x in result.keys():
        for part in result[x]:
            spans.append([x, part[0], len(part[1])])

    return spans

result = read_result()
spans = generate_spans(result)


from BlockSelector import BlockSelector
bs = BlockSelector(spans)
bs.find_best_match(0, 1)

result = bs.get_best_match_haplos()

print(result)
with open(f'./result/hotspots.txt', 'w') as f:
    f.write("%s\n" % result)