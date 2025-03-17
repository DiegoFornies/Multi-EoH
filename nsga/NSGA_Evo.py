from abc import ABC, abstractmethod
from reader import Reader
from llm import LLMManager
from nsga.Individual import Individual
from nsga.Population import Population
import random

class NSGA_Evo(ABC):
    def __init__(self, problem_name, population_size, objective_functions, reference_vectors = ''):
        self.Reader = Reader(problem_name)
        self.LLMManager = LLMManager()

        self.population_size = population_size
        self.population = Population(population_size, self.LLMManager, self.Reader)
        self.problem_name = problem_name

        self.instances = self.get_instances()

        self.of = self.init_objective_functions_info(objective_functions)

        self.reference_vectors = reference_vectors

    def init_objective_functions_info(self, objective_functions):
        for of_name, of_info in objective_functions.items():
            of_info['max_score'] = {}
            of_info['min_score'] = {}
            for name, _ in self.instances.items():
                of_info['min_score'][name] = float('inf')
                of_info['max_score'][name] = float('-inf')

        return objective_functions
    
    def select_parents(self): #selecciona los padres y los pone en la población, eliminando los demás.
        if len(self.of) <= 3:
            parents = self.population.select_parents_II(self.of)
        else:
            parents = self.population.select_parents_III(self.reference_vectors)
        return parents

    def get_instances(self):
        instances = self.Reader.get_instances()
        decoded_ins = {}
        for name, instance in instances.items():
            decoded_ins[name] = self.decode_instance(instance)
        return decoded_ins
    
    def reflection(self, clusters):
        clusters_reflection = []
        for cluster, info in clusters.items():
            system_prompt, user_prompt = self.Reader.get_cluster_reflection(info, self.of)
            ref = self.LLMManager.get_reflection(system_prompt, user_prompt)
            clusters_reflection.append({'Centroid': info['Centroid'], 'Reflection': ref})
        system_prompt, user_prompt = self.Reader.get_long_reflection(clusters_reflection, self.of)
        general_reflection = self.LLMManager.get_reflection(system_prompt, user_prompt)
        return general_reflection
    
    def start(self, k):
        self.population.init_population()
        self.population.evaluate_population(self.instances, self.objective_functions, self.feasibility, self.of)
        parents = self.select_parents()
        parents.print_population()
        clusters = self.population.get_k_means(k)
        self.reflection(clusters)
        print(clusters)

    @abstractmethod
    def feasibility(self, instance, solution):
        pass

    @abstractmethod
    def objective_functions(self, individual): #return a dictionary with key: name of the objective function, value: fitness in the objective function
        pass

    @abstractmethod
    def decode_instance(self, individual): #return a dictionary with key: name of the objective function, value: fitness in the objective function
        pass