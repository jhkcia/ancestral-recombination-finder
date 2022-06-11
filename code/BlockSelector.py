DEBUG = False

def find_mosaic_score(mosaic, Rho):
    K=mosaic[4]
    T_est = mosaic[3]/1000
    L = mosaic[1]-mosaic[0]+1
    removal = mosaic[2]
    h_score =(1/2)*K*Rho*T_est # *L
    return h_score

class BlockState:
    def __init__(self, score, previous):
        self.score = score
        self.previous = previous
    def __str__(self) -> str:
        return f'{self.score}, {self.previous}'

class BlockSelector:
    def __init__(self, mosaics):
        self.mosaics = mosaics
        self.last_position = max(list(zip(*self.mosaics))[1])
        self.first_position = min(list(zip(*self.mosaics))[0])
        self.states = {}
        self.positions = self.get_positions()

    def _get_mosaics_end_in(self, index):
        result = []
        for x in self.mosaics:
            if x[1] == index:
                result.append(x)
        return result

    def get_positions(self):
        l1 = list(list(zip(*self.mosaics))[0])
        l2 = list(list(zip(*self.mosaics))[1])
        l2.extend(l1)
        l= list(set(l2))
        l.sort()
        return l

    def find_best_match(self, removal_score):

        for i in range(len(self.positions)):
            pos = self.positions[i] 
                       
            DEBUG and print(f'checking index {i}, position {pos}')
            if i==0:
                self.states[pos] = BlockState(0, None)
            else:
                min_score = 9999999999
                
                for mosaic in self._get_mosaics_end_in(pos):
                    previous_index = mosaic[0]
                    h_score = find_mosaic_score(mosaic, removal_score)
                    current_score = self.states[previous_index].score+ h_score
                    if current_score< min_score:
                        min_score = current_score
                        self.states[pos] = BlockState(min_score, previous_index)
            DEBUG and print(self.states[pos])
            # DEBUG and print(self.states[pos])

    def get_best_match_mosaics(self):
        result = []
        index = self.last_position
        while index!=None:
            result.append(index)
            index = self.states[index].previous
        result.reverse()
        return result

    def get_mosaic_removal(self, start, end):
        for h in self.mosaics:
            if h[0]==start and h[1]==end:
                return h[2]
        raise Exception( f'mosaic not found for {start}-{end}')

    def get_statistics(self):
        removal = 0
        mosaics = 0

        index = self.last_position
        while True:
            state = self.states[index]
            if state.previous == None:
                break

            mosaics+=1
            removal+=self.get_mosaic_removal(state.previous, index)
            index = state.previous

        DEBUG and print(f'#Removal={removal}, #Mosaics = {mosaics}')
        return removal, mosaics
        


