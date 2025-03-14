from nsga import NSGA_Evo
from utils import objective_functions, decode_instance, feasibility

#reference_vectors es una lista donde cada elemento es un vector en lista

class NSGA_Evo_JSSP(NSGA_Evo):
    def __init__(self, problem_name, population_size, reference_vectors = ''):
        objective_functions = {'Makespan': {'Objective': 'Minimize'}, 
                               'Separation': {'Objective': 'Minimize'}, #escribir el nombre que hay en objective_functions.py para cada una con su objetivo (minimizar o maximizar)
                               'Balance': {'Objective': 'Minimize'}}
        super().__init__(problem_name, population_size, objective_functions, reference_vectors)

    def feasibility(self, instance, solution): #return True if the solution is feasible and False if it is not.
        return feasibility(instance, solution)

    def objective_functions(self, individual): #return a dictionary with key: name of the objective function, value: fitness in the objective function
        return objective_functions(individual)

    def decode_instance(self, instance): #return the instance in the input format given to the LLM in the prompt
        return decode_instance(instance)