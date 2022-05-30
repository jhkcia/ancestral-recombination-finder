DEBUG = False
class BlockState:
    def __init__(self, score, previous, kind):
        self.score = score
        self.previous = previous
        self.kind = kind
    def __str__(self) -> str:
        return f'{self.score}, {self.previous}, {self.kind}'
class BlockSelector:
    def __init__(self, haplos, total_population_size):
        self.haplos = haplos
        self.min_index = self._get_start_snp()
        self.max_index = self._get_last_snp()
        self.states = {}
        self.positions = self.get_positions()
        self.total_population_size = total_population_size

    def _get_last_snp(self):
        return max(list(zip(*self.haplos))[1])

    def _get_start_snp(self):
        return min(list(zip(*self.haplos))[0])
    
    def _get_haplos_end_in(self, index):
        result = []
        for x in self.haplos:
            if x[1] == index:
                result.append(x)
        return result

    def get_positions(self):
        l1 = list(list(zip(*self.haplos))[0])
        l2 = list(list(zip(*self.haplos))[1])
        l2.extend(l1)
        l= list(set(l2))
        l.sort()
        return l

    def get_haplo_length(self, start, end):
        # aya length moheme ya tedade SNP ha?
        return len([p for p in self.positions if (p>start and p<end)])+1


    def find_best_match(self, removal_score):

        for i in range(len(self.positions)):
            pos = self.positions[i] 
                       
            DEBUG and print(f'checking index {i}, position {pos}')
            if i==0:
                self.states[pos] = BlockState(0, None, None)
            else:
                prev_pos = self.positions[i-1] 
                min_score = self.states[prev_pos].score + 1
                self.states[pos] = BlockState(min_score, prev_pos, 'Recombinatoin')
                
                for haplo in self._get_haplos_end_in(pos):
                    previous_index = haplo[0]
                    haplo_score = self.states[previous_index].score+removal_score * (haplo[2]/(self.get_haplo_length(haplo[0], haplo[1], )*self.total_population_size))
                    if haplo_score< min_score:
                        min_score = haplo_score
                        self.states[pos] = BlockState(min_score, previous_index, 'Block')
            DEBUG and print(self.states[pos])

    def get_best_match_haplos(self):
        result = []
        index = self.max_index
        # print(self.states)
        while index!=None:
            result.append(index)
            # print(index)
            index = self.states[index].previous
        result.reverse()
        return result

    def get_haplo_removal(self, start, end):
        for h in self.haplos:
            if h[0]==start and h[1]==end:
                return h[2]
        raise 'haplo not found'

    def get_statistics(self):
        recombinations = 0
        removal = 0
        haplos = 0

        index = self.max_index
        while index!=None:
            state = self.states[index]
            if state.kind=='Block':
                haplos+=1
                removal+=self.get_haplo_removal(state.previous, index)
            elif state.kind == 'Recombinatoin':
                recombinations+=1

            index = state.previous
        if haplos>0:
            haplos-=1
        print(f'recomb = {recombinations}, removal={removal}, haplos = {haplos}')
        return removal, recombinations+haplos
        


