import tsinfer
import tsdate
class TimeFinder:
    def __init__(self, haplos, population, mutations):
        self.haplos = haplos
        self.min_index = self._get_start_snp()
        self.max_index = self._get_last_snp()
        self.positions = self.get_positions()
        self.population = population
        self.mutations_dict = self._generate_mutation_dict(mutations)


    def _generate_mutation_dict(self, mutation_df):
        mutation_dict = dict()
        for i, row in mutation_df.iterrows():
            key = f"{row['position']}__{row['sample']}"
            mutation_dict[key] = True
        return mutation_dict

    def get_positions(self):
        l1 = list(list(zip(*self.haplos))[0])
        l2 = list(list(zip(*self.haplos))[1])
        l2.extend(l1)
        l= list(set(l2))
        l.sort()
        return l

    def _get_last_snp(self):
        return max(list(zip(*self.haplos))[1])

    def _get_start_snp(self):
        return min(list(zip(*self.haplos))[0])
    
    def find_mrca_time(self, start, end, removal):
        positions = [p for p in self.positions if p>=start and p<=end]
        L = max(positions)- min(positions)+1
        start = min(positions)
        sites = []
        individuals = [p for p in self.population if not p in removal]
        for p in positions:
            states = []
            for sample in individuals:
                if f"{p}__{sample}" in self.mutations_dict:
                    states.append(1)
                else:
                    states.append(0)
            sites.append([p, states])
        with tsinfer.SampleData(sequence_length=L) as sample_data:
            for record in sites:
                sample_data.add_site(record[0]-start, record[1], ["A", "T"])

        inferred_ts = tsinfer.infer(sample_data)
        dated_ts = tsdate.date(inferred_ts, Ne=10000, mutation_rate=1e-8)
        T =  dated_ts.max_root_time
        print(T)
        return T

    def find_all_times(self):
        H = []
        for h in self.haplos:
            t = self.find_mrca_time(h[0], h[1], h[2])
            H.append([h[0], h[1], len(h[2], t)])
        return H