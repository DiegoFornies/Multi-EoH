from nsga import NSGA_Evo_JSSP
from reader import Reader

population_size = 20
iterations = 25

try:
    NSGA = NSGA_Evo_JSSP('jssp', population_size=population_size, iterations = iterations, crossover_type='II')
    NSGA.start()
except Exception as e:
    NSGA = NSGA_Evo_JSSP('jssp', population_size=population_size, iterations = iterations, crossover_type='II')
    NSGA.start()

NSGA = NSGA_Evo_JSSP('jssp', population_size=population_size, iterations = iterations, crossover_type='I')

NSGA.start()