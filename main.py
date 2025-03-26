from nsga import NSGA_Evo_JSSP
from reader import Reader

population_size = 20
iterations = 20

NSGA = NSGA_Evo_JSSP('jssp', population_size=population_size, iterations = iterations, execution_name='')
NSGA.start()

#NSGA = NSGA_Evo_JSSP('jssp', population_size=population_size, iterations = iterations, crossover_type='I')