from nsga import NSGA_Evo_JSSP
from reader import Reader

NSGA = NSGA_Evo_JSSP('jssp', population_size=5, iterations = 2, execution_name='Explotacion', crossover_type='I')

NSGA.start()