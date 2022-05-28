class BlockState:
    def __init__(self, score, previous):
        self.score = score
        self.previous = previous
    
class BlockSelector:
    def __init__(self, haplos):
        self.haplos = haplos
        self.min_index = self._get_start_snp()
        self.max_index = self._get_last_snp()
        self.states = {}
        self.positions = self.get_positions()
    
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


    def find_best_match(self, removal_score, recombination_score):
        self.removal_score = removal_score
        self.recombination_score = recombination_score

        for i in range(len(self.positions)):
            pos = self.positions[i] 
                       
            print(f'checking index {i}, position {pos}')
            if i==0:
                self.states[pos] = BlockState(0, None)
            else:
                prev_pos = self.positions[i-1] 
                min_score = self.states[prev_pos].score + self.recombination_score
                self.states[pos] = BlockState(min_score, prev_pos)
                
                for haplo in self._get_haplos_end_in(pos):
                    previous_index = haplo[0]
                    haplo_score = self.states[previous_index].score+self.removal_score * haplo[2]
                    if haplo_score< min_score:
                        min_score = haplo_score
                        self.states[pos] = BlockState(min_score, previous_index)
                        
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