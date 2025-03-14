from abc import ABC, abstractmethod
from reader import Reader
from llm import LLMManager
from utils import calculate_crowding_distance, calculate_distances_to_reference_vectors
from nsga.Individual import Individual
import random

class NSGA_Evo(ABC):
    def __init__(self, problem_name, population_size, objective_functions, reference_vectors = ''):
        self.Reader = Reader(problem_name)
        self.population_size = population_size
        self.population = []
        self.LLMManager = LLMManager()
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

    def init_population(self):
        for n in range(self.population_size):
            system_prompt, user_prompt = self.Reader.get_initialization_prompt()
            individual = self.create_individual(system_prompt, user_prompt)
            self.population.append(individual)

    def create_individual(self, system_prompt, user_prompt):
        description, code = self.LLMManager.get_heuristic(system_prompt, user_prompt)
        return Individual(description, code)
    
    def evaluate_population(self):
        for individual in self.population:
            feasible = individual.evaluate(self.instances, self.objective_functions, self.feasibility, self.of) #guarda la evaluación en individual y devuelve si es feasible o no
            if not feasible:
                self.population.remove(individual) #eliminamos los individuos que sean infeasibles
        self.update_minmax_score()
        self.normalize_and_mean_population()

    def update_minmax_score(self):
        for individual in self.population:
            self.of = individual.update_minmax(self.of)
    
    def normalize_and_mean_population(self):
        num_instances = len(self.instances)
        for individual in self.population:
            individual.normalize(self.of)
            individual.average(self.of, num_instances)
    
    def get_instances(self):
        instances = self.Reader.get_instances()
        decoded_ins = {}
        for name, instance in instances.items():
            decoded_ins[name] = self.decode_instance(instance)
        return decoded_ins
    
    def select_parents(self): #selecciona los padres y los pone en la población, eliminando los demás.
        if len(self.of) <= 3:
            self.population = self.select_parents_II()
        else:
            self.population = self.select_parents_III()
    
    def select_parents_II(self): #utilizando NSGA II
        if len(self.population) > self.population_size: #por si existe menos población que population_size debido a infeasibles
            global_front = []
            num_parents = 0
            current_population = self.population
            while not num_parents == self.population_size:
                front, current_population = self.get_pareto_front(current_population) #el resto de la población se pone en current_population para siguiente frontera
                if num_parents + len(front) <= self.population_size:
                    global_front.extend(front)
                    num_parents += len(front)
                else:
                    calculate_crowding_distance(front)
                    front_sorted = sorted(front, key=lambda x: x['crowding_distance'], reverse=True)
                    remaining = self.population_size - num_parents
                    global_front.extend(front_sorted[:remaining])
                    num_parents += remaining

            return global_front
        else:
            return self.population

    def select_parents_III(self): #utilizando NSGA III
        k = self.population_size // len(self.reference_vectors)
        rest = self.population_size % len(self.reference_vectors) #iremos añadiendo el resto por orden de vector referencia
        groups = self.get_groups_reference_vectors(k, rest)
        front = []
        for key, value in groups.items():
            front.extend(value)
        return front
    
    def get_groups_reference_vectors(self, k, rest = 0): #k es los k mejores de cada uno, y rest por si sobran
        calculate_distances_to_reference_vectors(self.population, self.reference_vectors)
        groups = {}
        for reference_vector in self.reference_vectors:
            sorted_population = sorted(self.population, key=lambda ind: ind.vector_distance[reference_vector], reverse=True)
            if rest > 0:
                groups[reference_vector] = sorted_population[:k + 1]
                rest -= 1
            else:
                groups[reference_vector] = sorted_population[:k]
        return groups
    
    def get_pareto_front(self, current_population):
        pareto_front = []
        rest = []
        for individual in current_population:
            dominated = individual.get_dominance(current_population)
            if not dominated:
                pareto_front.append(individual)
            else:
                rest.append(individual)
        return pareto_front, rest

    @abstractmethod
    def feasibility(self, instance, solution):
        pass

    @abstractmethod
    def objective_functions(self, individual): #return a dictionary with key: name of the objective function, value: fitness in the objective function
        pass

    @abstractmethod
    def decode_instance(self, individual): #return a dictionary with key: name of the objective function, value: fitness in the objective function
        pass