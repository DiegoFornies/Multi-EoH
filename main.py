from nsga import NSGA_Evo_JSSP
from reader import Reader

NSGA = NSGA_Evo_JSSP('jssp', population_size=10, k = 3, iterations = 5)

best_individuals = NSGA.start()

for individual in best_individuals:
    