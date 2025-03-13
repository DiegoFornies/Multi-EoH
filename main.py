from nsga import NSGA_Evo_JSSP
from reader import Reader
NSGA = NSGA_Evo_JSSP('jssp', 1)

NSGA.init_population()
NSGA.evaluate_population()
for i in range(1):
    print(NSGA.population[i]['Evaluation'])