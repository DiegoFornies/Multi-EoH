from abc import ABC, abstractmethod
from reader import Reader
from llm import LLMManager
import random

class NSGA_Evo(ABC):
    def __init__(self, problem_name, population_size, objective_functions):
        self.Reader = Reader(problem_name)
        self.population_size = population_size
        self.population = []
        self.LLMManager = LLMManager()
        self.instances = self.get_instances()
        self.of = self.init_objective_functions_info(objective_functions)

    def init_objective_functions_info(self, objective_functions):
        for of_name, of_info in objective_functions.items():
            of_info['max_score'] = {}
            of_info['min_score'] = {}
            for name, _ in self.instances.items():
                of_info['min_score'][name] = float('inf')
                of_info['max_score'][name] = float('-inf')

        return objective_functions

    def init_population(self):
        for n in range(self.population_size):
            system_prompt, user_prompt = self.Reader.get_initialization_prompt()
            description, code = self.create_individual(system_prompt, user_prompt)
            self.population.append({'Description' : description, 'Code': code})

    def create_individual(self, system_prompt, user_prompt):
        description, code = self.LLMManager.get_heuristic(system_prompt, user_prompt)
        return (description, code)
    
    def evaluate_population(self):
        for individual in self.population:
            evaluation = self.evaluate_individual(individual)
            individual['Evaluation'] = evaluation
        self.update_minmax_score()
        self.normalize_population()
        self.mean_population()

    def update_minmax_score(self):
        for of_name, of_info in self.of.items():
            for individual in self.population:
                if not individual['Evaluation']:
                    break
                else:
                    for inst_name, inst_ev in individual['Evaluation'].items():
                        if of_info['min_score'][inst_name] > inst_ev[of_name]:
                            of_info['min_score'][inst_name] = inst_ev[of_name]
                        if of_info['max_score'][inst_name] < inst_ev[of_name]:
                            of_info['max_score'][inst_name] = inst_ev[of_name]
    
    def normalize_population(self):
        for of_name, of_info in self.of.items():
            for individual in self.population:
                if not individual['Evaluation']:
                    pass
                else:
                    for inst_name, inst_ev in individual['Evaluation'].items():
                        min = of_info['min_score'][inst_name]
                        max = of_info['max_score'][inst_name]
                        divisor = max - min
                        if divisor == 0:
                            divisor = 1 #solo se cumple si todos tienen el mismo fitness
                        value = (max - inst_ev[of_name]) / divisor
                        if of_info['Objective'] == 'Maximize':
                            value = 1 - value

                        inst_ev[of_name] = value
    
    def mean_population(self):
        num_instances = len(self.instances)
        for individual in self.population:
                mean_evaluation = {}
                if not individual['Evaluation']:
                    pass
                else:
                    for of_name, of_info in self.of.items():
                        sum = 0
                        for inst_name, inst_ev in individual['Evaluation'].items():
                            sum += inst_ev[of_name]
                        mean_evaluation[of_name] = sum / num_instances

    def evaluate_individual(self, individual): #return a dictionary of objective function values
        solutions = self.get_individual_solution(individual)
        evaluation = {}
        for instance_name, solution in solutions.items():
            evaluation[instance_name] = {}
            #if self.feasibility(self.instances[instance_name], solution):
            results = self.objective_functions(solution)
            for of_name, _ in self.of.items():
                evaluation[instance_name][of_name] = results[of_name]
            #else:
            #    return False
        return evaluation

    def get_individual_solution(self, individual):
        code = individual['Code']
        local_vars = {}
        exec(code, globals(), local_vars)
        heuristic = local_vars['heuristic']
        solutions = {}
        for name, instance in self.instances.items():
            solutions[name] = heuristic(instance)
        del local_vars['heuristic']
        return solutions
    
    def get_instances(self):
        instances = self.Reader.get_instances()
        decoded_ins = {}
        for name, instance in instances.items():
            decoded_ins[name] = self.decode_instance(instance)
        return decoded_ins

    @abstractmethod
    def feasibility(self, instance, solution):
        pass

    @abstractmethod
    def objective_functions(self, individual): #return a dictionary with key: name of the objective function, value: fitness in the objective function
        pass

    @abstractmethod
    def decode_instance(self, individual): #return a dictionary with key: name of the objective function, value: fitness in the objective function
        pass