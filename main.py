from nsga import NSGA_Evo_JSSP
from reader import Reader

NSGA = NSGA_Evo_JSSP('jssp', population_size=3)

NSGA.start(k=1)
print(NSGA.of)