from nsga import NSGA_Evo_JSSP
from reader import Reader

NSGA = NSGA_Evo_JSSP('jssp', population_size=10, k = 3, iterations = 5)

NSGA.start()