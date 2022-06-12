def create_empty_dict(length):
    result = dict()
    for i in range(pow(2, length)):
        item = f'{i:b}'.zfill(length)
        result[item] = 0
    return result

class SpanFinder:
    def __init__(self, vcf_df, print_logs):
        self.print_log = print_logs
        self.vcf_df = vcf_df
        self.samples = list(vcf_df.index)
        self.positions = list(vcf_df.columns)
        self.positions.sort()

    def find_combinations(self, position1, position2, ignored):
        self.print_log and print(f'find_combinations for positions {position1}, {position2}')
        samples = [s for s in self.samples if not s in ignored]
        
        khkh =self.vcf_df.loc[samples]
        gg = khkh.value_counts(subset=[position1, position2 ])
        dc = create_empty_dict(2)
        for x in  gg.keys():
            s = str(x[0])+str(x[1])
            dc[s] = gg[x]

#             print (f'{x},, {gg[x]}')
        
        
        self.print_log and print(f'combinations for positions {position1}, {position2} :{dc}')
        min_snp =9999999999
        min_haplo =''

        for i in range(0, 2):
            for j in range(0, 2):
                s = str(i)+str(j)
                if dc[s]<min_snp:
                    min_snp=dc[s]
                    min_haplo =s
        i =int(min_haplo[0])
        j =int(min_haplo[1])
        inconsistant_samples =list(self.vcf_df[(self.vcf_df[position1]==i) & (self.vcf_df[position2]==j)].index)

        return inconsistant_samples, dc, min_haplo

    def find_next_position(self, position):
        next_positions = position
        later = [x for x in self.positions if x>position]
        if len(later)>0:
            next_positions = later[0]
        return next_positions

    def remove_samples (self, new_df, inconsistant_samples ):
        self.print_log and print(f'removing samples {inconsistant_samples}')
        return new_df[~new_df['sample'].isin(inconsistant_samples)]

    def find_all_spans(self, threshold_percent, start, end):
        result = []

        for index, p in enumerate(self.positions):
            if index<start:
                continue

            if index>end:
                print('LIMIT EXCEED ')
                break
            print(f'checking position {index+1} of {len(self.positions)}')
            r = self.find_spans(p, threshold_percent)
            result.append([p, r])
            print(f"Done with length ={len(r)}")
        return result

    ## better
    def find_spans(self, position, threshold_percent):
        self.print_log and print(f'position is {position}')
        current_position = position
        jojo = 0
        DATA = []
        sample_count = len(self.samples)
        prev_positions = []
        to_remove = set()
        while True:
            jojo+=1
            if(jojo % 10 == 0):
                self.print_log and print(f"processed {jojo} variant, remaining samples {len(new_df['sample'].unique())}")
                # break
            # if a position removed by removing some samples? should we return the span that finishes in that position?
            prev_positions.append(current_position)
            next_position = self.find_next_position(current_position)
            self.print_log and print(f'checking position {next_position}')
            if current_position==next_position:
                self.print_log and print('Arrive to end.')
                break
            for position in prev_positions:
                samples, statistics, haplo = self.find_combinations(position, next_position, to_remove)
                #TODO improve removing mechanisem!!!!
                to_remove.update(set(samples))
            current_position = next_position
            if len(to_remove)>0:
                to_remove= set(to_remove)
                total_remove=len(to_remove)
                if total_remove > sample_count*threshold_percent/100:
                    self.print_log and print('max threshold arrived in position '+str(current_position))
                    break
#                 new_df = self.remove_samples(new_df, to_remove)
            # print(f'adding data {position} || {current_position} || {to_remove}')
            DATA.append([current_position, list(to_remove)])

        return DATA