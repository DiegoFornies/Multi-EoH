from nsga import NSGA_Evo_JSSP
from reader import Reader
NSGA = NSGA_Evo_JSSP('jssp', 1)

NSGA.init_population()
NSGA.evaluate_population()

NSGA.population[0]['Evaluation']

#print(NSGA.Reader.get_initialization_prompt())