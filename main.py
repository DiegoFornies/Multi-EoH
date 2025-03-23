from nsga import NSGA_Evo_JSSP
from reader import Reader

NSGA = NSGA_Evo_JSSP('jssp', population_size=20, iterations = 20, execution_name='CrossoverExplotacion_Reflection_Gemini2')

NSGA.start()