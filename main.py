from nsga import NSGA_Evo_JSSP
from reader import Reader

population_size = 20
iterations = 25

NSGA = NSGA_Evo_JSSP('jssp', population_size=population_size, iterations = iterations, execution_name='ExplotacionReflectionGemini', crossover_type='I')
#NSGA = NSGA_Evo_JSSP('jssp', population_size=20, iterations = 25, execution_name='ExploracionReflectionGemini', crossover_type='II')

NSGA.start()