import numpy as np
import pandas as pd

def create_empty_dict(length):
    result = dict()
    for i in range(pow(2, length)):
        item = f'{i:b}'.zfill(length)
        result[item] = 0
    return result

class SpanFinder:
    def __init__(self, mutations_df, samples, print_logs = False):
        self.mutations_df = mutations_df
        self.samples = samples
        self.positions = mutations_df.position.unique()
        self.positions.sort()
        self.print_log = print_logs

    def find_combinations(self, position1, position2, filtered_mutations_df):
        self.print_log and print(f'find_combinations for positions {position1}, {position2}')

        df1 = filtered_mutations_df[filtered_mutations_df['position']==position1]
        df2 = filtered_mutations_df[filtered_mutations_df['position']==position2]
        df_m = pd.merge(df1, df2,how='outer',left_on=['sample'], right_on=['sample'] ).fillna(0)
        df_g = df_m.groupby(['state_x', 'state_y']).agg('count')
        dc = create_empty_dict(2)
#         print(df_g)
        for idx, row in df_g.iterrows():
            for i in range(0, 2):
                for j in range(0, 2):
                    s = str(i)+str(j)
                    if row.name[0]==i and row.name[1]==j:
                        dc[s] =row['sample']
        dc['00']=len(self.samples)-np.sum(list(dc.values()))
        self.print_log and print(f'combinations for positions {position1}, {position2} :{dc}')
        min_snp =9999999999
        min_haplo =''

        for i in range(0, 2):
            for j in range(0, 2):
                s = str(i)+str(j)
                if dc[s]<min_snp:
                    min_snp=dc[s]
                    min_haplo =s
        if min_haplo=='00':
            current_samples = df_m['sample'].unique()
            inconsistant_samples = [x for x in self.samples if (x not in current_samples)]
        else:
            i =int(min_haplo[0])
            j =int(min_haplo[1])
            inconsistant_samples = df_m[(df_m['state_x']==i) & (df_m['state_y']==j)]['sample'].unique()
            inconsistant_samples
        return inconsistant_samples, dc, min_haplo

    def find_next_position(self, position):
        next_positions = position
        if self.positions[self.positions>position].any():
            next_positions = self.positions[self.positions>position][0]
        return next_positions

    def remove_samples (self, new_df, inconsistant_samples ):
        self.print_log and print(f'removing samples {inconsistant_samples}')
        return new_df[~new_df['sample'].isin(inconsistant_samples)]

    def find_all_spans(self, threshold_percent):
        result = []
        for index, p in enumerate(self.positions):
            print(f'checking position {index+1} of {len(self.positions)}')
            r = self.find_spans(p, threshold_percent)
            result.append([p, r])
        return result
    
    def find_spans(self, position, threshold_percent):
        self.print_log and print(f'position is {position}')
        new_df = self.mutations_df
        current_position = position
        jojo = 0
        DATA = []
        sample_count = len(self.samples)
        total_remove = 0
        prev_positions = []
        while True:
            jojo+=1
            if(jojo % 10 == 0):
                self.print_log and print(f"processed {jojo} variant, remaining samples {len(new_df['sample'].unique())}")
                # break
            # if a position removed by removing some samples? should we return the span that finishes in that position?
            prev_positions.append(current_position)
            next_position = self.find_next_position(current_position)
            print(f'checking position {next_position}')
            if current_position==next_position:
                self.print_log and print('Arrive to end.')
                break
            to_remove = []
            for position in prev_positions:
                samples, statistics, haplo = self.find_combinations(position, next_position, new_df)
                #TODO improve removing mechanisem!!!!
                to_remove.extend(samples)
            current_position = next_position
            should_stop = False
            if len(to_remove)>0:
                to_remove= set(to_remove)
                total_remove+=len(to_remove)
                if total_remove > sample_count*threshold_percent/100:
                    self.print_log and print('max threshold arrived in position '+str(current_position))
                    break
                new_df = self.remove_samples(new_df, to_remove)

            DATA.append([current_position, to_remove])

        return DATA