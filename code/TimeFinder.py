import tsdate
import tsinfer
from math import floor
DEBUG = False


class TimeFinder:
    def __init__(self, haplos, population, mutations):
        self.haplos = haplos
        self.positions = self.get_positions(mutations)
        self.population = population
        self.mutations_dict = self._generate_mutation_dict(mutations)
        self.ts_list = []
    def _generate_mutation_dict(self, mutation_df):
        mutation_dict = dict()
        for i, row in mutation_df.iterrows():
            key = f"{row['position']}__{row['sample']}"
            mutation_dict[key] = True
        return mutation_dict

    def get_positions(self, mutation_df):
        l = [p for p in mutation_df['position'].unique()]
        l.sort()
        return l

    def find_mrca_time(self, start, end, removal, mutation_rate=1e-8):
        positions = [p for p in self.positions if p >= start and p <= end]
        L = floor(end - start+1)
        DEBUG and print(
            f'start finding tmrca for position {start} to {end} with Length {L}')
        start = floor(start)
        sites = []
        individuals = [p for p in self.population if not p in removal]
        for p in positions:
            states = []
            for sample in individuals:
                keyy = f"{p}__{sample}"
                if keyy in self.mutations_dict:
                    DEBUG and print(keyy)
                    states.append(1)
                else:
                    states.append(0)
            sites.append([p, states])
        with tsinfer.SampleData(sequence_length=L) as sample_data:
            for record in sites:
                sample_data.add_site(record[0]-start, record[1], ["A", "T"])
        DEBUG and print(f'start inferring time ')
        inferred_ts = tsinfer.infer(sample_data)
        DEBUG and print(
            f'start inferring date  for {inferred_ts.num_trees} Trees')
        simplified_tree = tsdate.preprocess_ts(inferred_ts)
        dated_ts = tsdate.date(simplified_tree, Ne=10000,
                               mutation_rate=mutation_rate)
        T = dated_ts.max_root_time
        self.ts_list.append([min(positions), max(positions),inferred_ts, T, sites, self.mutations_dict])
        DEBUG and print(T)
        return T

    def find_all_times(self):
        H = []
        for index, h in enumerate(self.haplos):
            if index % 2 == 0:
                print(f'inferring {index+1} of {len(self.haplos)}')
            t = self.find_mrca_time(h[0], h[1], h[2])
            H.append([h[0], h[1], len(h[2]), t])
        return H
