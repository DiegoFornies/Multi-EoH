from nsga import NSGA_Evo_JSSP

initial_population = 30
population_size = 10
iterations = 10

for reflection in [True, False]:
    NSGA = NSGA_Evo_JSSP('jssp', initial_population = initial_population, population_size=population_size, iterations = iterations, reflection = reflection)
    NSGA.start()