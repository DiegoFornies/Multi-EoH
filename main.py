from nsga import NSGA_Evo_JSSP

population_size = 10
iterations = 10

NSGA = NSGA_Evo_JSSP('jssp', population_size=population_size, iterations = iterations, execution_name='')
NSGA.start()