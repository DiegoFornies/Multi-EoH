from reader import Reader
from nsga.Individual import Individual
from llm import LLMManager
from utils import calculate_crowding_distance, calculate_distances_to_reference_vectors
from sklearn.cluster import KMeans
import numpy as np

class Population():
    def __init__(self, population_size, llmManager, reader, population = []):
        self.population_size = population_size
        self.population = population
        self.LLMManager = llmManager
        self.Reader = reader

    def init_population(self):
        for n in range(self.population_size):
            system_prompt, user_prompt = self.Reader.get_initialization_prompt()
            individual = self.create_individual(system_prompt, user_prompt)
            self.add_individual(individual)

    def create_subpopulation(self, population):
        return Population(self.population_size, self.LLMManager, self.Reader, population)

    def create_individual(self, system_prompt, user_prompt):
        description, code = self.LLMManager.get_heuristic(system_prompt, user_prompt)
        return Individual(description, code)
    
    def add_individual(self, individual):
        self.population.append(individual)
    
    def evaluate_population(self, instances, objective_functions, feasibility, of): #evalúa la población, la normaliza y la media.
        for individual in list(self.population):
            individual.evaluate(instances, objective_functions, feasibility, of) #guarda la evaluación en individual y devuelve si es feasible o no
            if individual.evaluation == 'Infeasible':
                print(f'El heurístico {individual.id} no es feasible, se elimina.')
                self.population.remove(individual) #eliminamos los individuos que sean infeasibles
            if individual.evaluation == 'Code Error':
                print(f'El heurístico {individual.id} tiene errores en el código, se elimina.')
                self.population.remove(individual)
        self.update_minmax_score(of)
        self.normalize_and_mean_population(of, instances)

    def update_minmax_score(self, of):
        self.print_population()
        for individual in self.population:
            self.of = individual.update_minmax(of)
    
    def normalize_and_mean_population(self, of, instances):
        num_instances = len(instances)
        for individual in self.population:
            individual.normalize(of)
            individual.average(of, num_instances)

    def select_parents_II(self, of): #utilizando NSGA II
        if len(self.population) > self.population_size: #por si existe menos población que population_size debido a infeasibles
            global_front = []
            num_parents = 0
            current_population = self.population
            while not num_parents == self.population_size:
                front, current_population = self.get_pareto_front(current_population, of) #el resto de la población se pone en current_population para siguiente frontera
                if num_parents + len(front) <= self.population_size:
                    global_front.extend(front)
                    num_parents += len(front)
                else:
                    calculate_crowding_distance(front)
                    front_sorted = sorted(front, key=lambda x: x.crowding_distance, reverse=True)
                    remaining = self.population_size - num_parents
                    global_front.extend(front_sorted[:remaining])
                    num_parents += remaining
            print('a')
            return self.create_subpopulation(global_front)
        else:
            return self

    def select_parents_III(self, reference_vectors): #utilizando NSGA III
        k = self.population_size // len(reference_vectors)
        rest = self.population_size % len(reference_vectors) #iremos añadiendo el resto por orden de vector referencia
        groups = self.get_groups_reference_vectors(reference_vectors, k, rest)
        front = []
        for key, value in groups.items():
            front.extend(value)
        return self.create_subpopulation(front)
    
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
    
    def get_pareto_front(self, current_population, of):
        pareto_front = []
        rest = []
        for individual in current_population:
            dominated = individual.get_dominance(of, current_population)
            if not dominated:
                pareto_front.append(individual)
            else:
                rest.append(individual)
        return pareto_front, rest
    
    def get_k_means(self, k):
        evaluations = np.array([list(ind.evaluation.values()) for ind in self.population])
        
        kmeans = KMeans(n_clusters=k, random_state=42)
        kmeans.fit(evaluations)
        clusters = {label:{'Individuals': self.create_subpopulation([]), 'Centroid': centroid} for label, centroid in enumerate(kmeans.cluster_centers_)} #guardamos centroide y individuo para cada cluster
        for ind, label in zip(self.population, kmeans.labels_):
            clusters[label]['Individuals'].add_individual(ind)
        
        return clusters
    
    def toString(self):
        text = ''
        for individual in self.population:
            text += f'Heuristic{individual.id}: \nDescription: {individual.description} \nCode: {individual.code}\n'
        return text
    
    def print_population(self):
        print(f'\nCantidad de individuos: {len(self.population)}')
        for individual in self.population:
            print(f'\nIndividuo {individual.id}: \n   Evaluación: {individual.evaluation}, Valid: {individual.valid}, Crowding Distance: {individual.crowding_distance}')