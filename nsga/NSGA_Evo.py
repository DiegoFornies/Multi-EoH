from abc import ABC, abstractmethod
from reader import Reader
from llm import LLMManager
from nsga.Individual import Individual
from nsga.Population import Population
import random
from utils import calculate_crowding_distance, calculate_distances_to_reference_vectors
import numpy as np
from sklearn.cluster import KMeans

class NSGA_Evo(ABC):
    def __init__(self, problem_name, population_size, objective_functions, reference_vectors = ''):
        self.Reader = Reader(problem_name)
        self.LLMManager = LLMManager()

        self.population_size = population_size
        self.population = []
        self.problem_name = problem_name

        self.crossover_iterations = self.population_size
        self.mutation_iterations = 3

        self.instances = self.get_instances()

        self.long_reflection = ''

        self.crossover_prob = {}

        self.of = self.init_objective_functions_info(objective_functions)

        self.reference_vectors = reference_vectors

        self.max_evolutions = 1

    def init_objective_functions_info(self, objective_functions):
        for _, of_info in objective_functions.items():
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
    
    def evaluate_population(self): #evalúa la población, la normaliza y la media.
        for individual in list(self.population):
            individual.evaluate(self.instances, self.objective_functions, self.feasibility, self.of) #guarda la evaluación en individual y devuelve si es feasible o no
            if individual.evaluation == 'Infeasible':
                print(f'El heurístico {individual.id} no es feasible, se elimina.')
                self.population.remove(individual) #eliminamos los individuos que sean infeasibles
            if individual.evaluation == 'Code Error':
                print(f'El heurístico {individual.id} tiene errores en el código, se elimina.')
                self.population.remove(individual)
        self.update_minmax_score(self.of)
        self.normalize_and_mean_population(self.of, self.instances)

    def update_minmax_score(self):
        self.print_population()
        for individual in self.population:
            self.of = individual.update_minmax(self.of)
    
    def normalize_and_mean_population(self):
        num_instances = len(self.instances)
        for individual in self.population:
            individual.normalize(self.of)
            individual.average(self.of, num_instances)
    
    def select_parents(self): #selecciona los padres y los pone en la población, eliminando los demás.
        if len(self.of) <= 3:
            parents = self.population.select_parents_II(self.of)
        else:
            parents = self.population.select_parents_III(self.reference_vectors)
        return parents

    def select_parents_II(self): #utilizando NSGA II
        if len(self.population) > self.population_size: #por si existe menos población que population_size debido a infeasibles
            global_front = []
            front_num = 0
            num_parents = 0
            current_population = self.population
            while not num_parents == self.population_size:
                front, current_population = self.get_pareto_front(current_population, self.of) #el resto de la población se pone en current_population para siguiente frontera
                calculate_crowding_distance(front)
                if num_parents + len(front) <= self.population_size:
                    num_parents += len(front)
                else:
                    calculate_crowding_distance(front)
                    front = sorted(front, key=lambda x: x.crowding_distance, reverse=True)
                    remaining = self.population_size - num_parents
                    front = front[:remaining]
                    num_parents += remaining
                for individual in front:
                    individual.front = front_num
                global_front.extend(front)
                front_num += 1
            return global_front
        else:
            calculate_crowding_distance(self.population)
            return self.population


    def select_parents_III(self): #utilizando NSGA III
        k = self.population_size // len(self.reference_vectors)
        rest = self.population_size % len(self.reference_vectors) #iremos añadiendo el resto por orden de vector referencia
        groups = self.get_groups_reference_vectors(self.reference_vectors, k, rest)
        front = []
        for key, value in groups.items():
            front.extend(value)
        return front
    
    def get_groups_reference_vectors(self, vectors, k, rest = 0): #k es los k mejores de cada uno, y rest por si sobran
        calculate_distances_to_reference_vectors(self.population, vectors)
        groups = {}
        for reference_vector in vectors:
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
            dominated = individual.get_dominance(self.of, current_population)
            if not dominated:
                pareto_front.append(individual)
            else:
                rest.append(individual)
        return pareto_front, rest
    
    def get_k_means(self, population, k):
        evaluations = np.array([list(ind.evaluation.values()) for ind in population])
        
        kmeans = KMeans(n_clusters=k, random_state=42)
        kmeans.fit(evaluations)
        clusters = {label:{'Individuals': [], 'Centroid': centroid} for label, centroid in enumerate(kmeans.cluster_centers_)} #guardamos centroide y individuo para cada cluster
        for ind, label in zip(population, kmeans.labels_):
            clusters[label]['Individuals'].append(ind)
        return clusters

    def get_instances(self):
        instances = self.Reader.get_instances()
        decoded_ins = {}
        for name, instance in instances.items():
            decoded_ins[name] = self.decode_instance(instance)
        return decoded_ins
    
    def update_reflection(self, clusters):
        clusters_reflection = []
        for cluster, info in clusters.items():
            system_prompt, user_prompt = self.Reader.get_cluster_reflection_prompt(info, self.of)
            ref = self.LLMManager.get_reflection(system_prompt, user_prompt)
            clusters_reflection.append({'Centroid': info['Centroid'], 'Reflection': ref})
        system_prompt, user_prompt = self.Reader.get_long_reflection_prompt(self.long_reflection, clusters_reflection, self.of)
        self.long_reflection = self.LLMManager.get_reflection(system_prompt, user_prompt)

    def tournament_selection_nsgaII(self, parents):

        parent1, parent2 = random.sample(parents, 2)

        if parent1.front < parent2.front:
            return parent1
        elif parent1.front > parent2.front:
            return parent2
        else:  
            if parent1.crowding_distance > parent2.crowding_distance:
                return parent1
            else:
                return parent2
            
    def crossover(self, parents): #sólo un crossover guiado por long_reflection entre dos padres
        sons = []
        for i in range(self.crossover_iterations):
            parent1 = self.tournament_selection_nsgaII(parents)
            parents_without_parent1 = list(filter(lambda p: p != parent1, parents))
            parent2 = self.tournament_selection_nsgaII(parents_without_parent1) #seleccionamos población sin parent2
            sCrossover_prompt, uCrossover_prompt = self.Reader.get_crossover_prompt(self.long_reflection, parent1, parent2)
            new_individual = self.LLMManager.get_heuristic(sCrossover_prompt, uCrossover_prompt) #Falta implementar prompt de crossover
            sons.append(new_individual)
        return sons
    
    def elitist_mutation(self, parents): #sólo una especie de mutación cogiendo los mejores individuos del frente pareto
        best_score = 0
        for individual in parents:
            if individual.evaluation['Mean'] > best_score:
                best_score = individual.evaluation['Mean']
                best_individual = individual
        sons = []
        for i in range(self.mutation_iterations):
            sMutation_prompt, uMutation_prompt = self.Reader.get_mutation_prompt(self.long_reflection, best_individual) #falta implementar prompt de mutation
            new_individual = self.LLMManager.get_heuristic(sMutation_prompt, uMutation_prompt)
            sons.append(new_individual)
        return sons
    
    def select_best_individuals(self): #TODO
        pass
          
    def start(self, k):
        self.population.init_population()
        for i in range(self.max_evolutions):
            self.population.evaluate_population(self.instances, self.objective_functions, self.feasibility, self.of)
            if len(self.population.population) == 0:
                print('No hay ningún heurístico válido.')
                return
            parents = self.select_parents()
            parents.print_population()
            clusters = self.population.get_k_means(k)
            self.update_reflection(clusters)

            crossover_sons = self.crossover(parents)
            mutation_sons = self.elitist_mutation(parents)

            parents.append(crossover_sons)
            parents.append(mutation_sons)

            self.population = parents
        self.select_best_individuals()

    @abstractmethod
    def feasibility(self, instance, solution):
        pass

    @abstractmethod
    def objective_functions(self, individual): #return a dictionary with key: name of the objective function, value: fitness in the objective function
        pass

    @abstractmethod
    def decode_instance(self, individual): #return a dictionary with key: name of the objective function, value: fitness in the objective function
        pass

    def print_population(self):
        print(f'\nCantidad de individuos: {len(self.population)}')
        for individual in self.population:
            print(f'\nIndividuo {individual.id}: \n   Evaluación: {individual.evaluation}, Valid: {individual.valid}, Crowding Distance: {individual.crowding_distance}')