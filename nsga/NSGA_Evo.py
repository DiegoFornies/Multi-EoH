from abc import ABC, abstractmethod
from reader import Reader
from llm import LLMManager
from nsga.Individual import Individual
import random
import numpy as np
from sklearn.cluster import KMeans
import os
from datetime import datetime
import time
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt
import pandas as pd
import json

class NSGA_Evo(ABC):
<<<<<<< HEAD
    def __init__(self, problem_name, population_size, objective_functions, iterations, execution_name, reflection, reference_vectors = ''):
=======
    def __init__(self, problem_name, population_size, objective_functions, iterations, execution_name, reference_vectors = ''):
        
>>>>>>> 1982cbc49940565d761245108c8cfb6617b87d10
        self.individual_id = 0

        self.Reader = Reader(problem_name)
        self.LLMManager = LLMManager()

        self.population_size = population_size
        self.population = []

        self.problem_name = problem_name

        self.mutation_prob = 0.1
        self.explorative_prob_init = 0.8
        self.intense_prob_init = 0.2
        self.explorative_prob_end = 0.2
        self.intense_prob_end = 0.8
        self.explorative_prob = self.explorative_prob_init
        self.intense_prob = self.intense_prob_init

        self.a = 10
        self.b = 0.4
        
        self.instances = self.get_instances()

        self.reflection = reflection
        self.long_reflectionI = ''
        self.long_reflectionII = ''


        self.of = objective_functions

        self.reference_vectors = reference_vectors

        self.max_evolutions = iterations
        self.iteration = 0

        self.whole_population = []

        if execution_name == '':
            execution_name = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        self.folder_path = os.path.join("ejecuciones", execution_name)
        self.create_execution_folder()

        self.individual_id = 0

        self.total_heuristics = 0
        self.correct_heuristics = 0
        self.infeasible_heuristics = 0
        self.incorrect_heuristics = 0
        self.repaired_heuristics = 0

        self.ks = []

    #---------------------------
    #------INITIALIZATIONS------
    #---------------------------
    
    def init_population(self):
        for n in range(self.population_size * 3):
            system_prompt, user_prompt = self.Reader.get_initialization_prompt()
            individual = self.create_individual(system_prompt, user_prompt)
            self.population.append(individual)

    def get_instances(self):
        instances = self.Reader.get_instances()
        decoded_ins = {}
        for name, instance in instances.items():
            decoded_ins[name] = self.decode_instance(instance)
        return decoded_ins
    
    #-------------------------------
    #------INDIVIDUAL CREATION------
    #-------------------------------

    def create_individual(self, system_prompt, user_prompt):
        code = self.LLMManager.get_heuristic(system_prompt, user_prompt)
        self.individual_id += 1
        self.total_heuristics += 1
        return Individual(code, self.Reader, self.LLMManager, self.folder_path, self.individual_id, self.iteration)

    #---------------------------
    #--------EVALUATIONS--------
    #---------------------------

    def evaluate_population(self): #evalúa la población, la normaliza y la media.
        for individual in list(self.population):
            if not individual.base_evaluation:
                individual.evaluate(self.instances, self.objective_functions, self.feasibility, self.of) #guarda la evaluación en individual y devuelve si es feasible o no
                if individual.base_evaluation == 'Infeasible':
                    print(f'El heurístico {individual.id} no es feasible, se elimina.')
                    self.infeasible_heuristics += 1
                    self.population.remove(individual) #eliminamos los individuos que sean infeasibles
                elif individual.base_evaluation == 'Code Error':
                    print(f'El heurístico {individual.id} tiene errores en el código, se elimina.')
                    self.incorrect_heuristics += 1
                    self.population.remove(individual)
                elif individual.repair_counter > 0:
                    self.repaired_heuristics += 1
                else:
                    self.correct_heuristics += 1
        self.normalize_and_mean_population()
    
    def normalize_and_mean_population(self):

        num_instances = len(self.instances)
        values = {inst_name : {of_name : [] for of_name, _ in self.of.items()} for inst_name, _ in self.population[0].base_evaluation.items()}

        for individual in self.population:
            for inst_name, inst_value in individual.base_evaluation.items():
                for of_name, of_value in inst_value.items():
                    values[inst_name][of_name].append(of_value)
            individual.normalized_evaluation = {inst_name : {of_name : 0 for of_name, _ in self.of.items()} for inst_name, _ in individual.base_evaluation.items()}
        
        for inst_name, inst_value in values.items():
            for of_name, of_value in inst_value.items():
                mean = np.mean(values[inst_name][of_name])
                std = np.std(values[inst_name][of_name])

                if std == 0:
                    std = 1

                for individual in self.population:
                    individual.normalized_evaluation[inst_name][of_name] = (individual.base_evaluation[inst_name][of_name] - mean) / std
                    if self.of[of_name]['Objective'] == 'Minimize':
                        individual.normalized_evaluation[inst_name][of_name] = - individual.normalized_evaluation[inst_name][of_name] #para la minimización cambiamos los signos

        num_instances = len(self.instances)
        for individual in self.population:
            individual.average(self.of, num_instances)
            individual.evaluated = True

    #-------------------------------
    #-------PARENTS SELECTION-------
    #-------------------------------

        #------------------------------------
        #-------NSGA II IMPLEMENTATION-------
        #------------------------------------

    def select_parents_II(self):
        global_front = []
        front_num = 0
        num_parents = 0
        current_population = self.population
        while (not num_parents == self.population_size) and len(current_population) > 0:
            front, current_population = self.get_pareto_front(current_population) #el resto de la población se pone en current_population para siguiente frontera
            self.calculate_crowding_distance(front)
            if num_parents + len(front) <= self.population_size:
                num_parents += len(front)
            else:
                self.calculate_crowding_distance(front)
                front = sorted(front, key=lambda x: x.crowding_distance, reverse=True)
                remaining = self.population_size - num_parents
                front = front[:remaining]
                current_population = front[remaining:]
                num_parents += remaining
            for individual in front:
                individual.front = front_num
            global_front.extend(front)
            front_num += 1
        return global_front, current_population
    
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
    
    def calculate_crowding_distance(self, front):
        num_ind = len(front)

        for ind in front:
            ind.crowding_distance = 0.0  

        for obj in front[0].evaluation.keys():
            front.sort(key=lambda ind: ind.evaluation[obj])

            front[0].crowding_distance = float("inf")
            front[-1].crowding_distance = float("inf")

            f_min = front[0].evaluation[obj]
            f_max = front[-1].evaluation[obj]
            
            if f_max == f_min:
                continue

            for i in range(1, num_ind - 1):
                front[i].crowding_distance += (front[i + 1].evaluation[obj] - front[i - 1].evaluation[obj]) / (f_max - f_min)

        #------------------------------------
        #-------NSGA III IMPLEMENTATION------ (NOT PROVED)
        #------------------------------------

    # def select_parents_III(self): #utilizando NSGA III
    #     k = self.population_size // len(self.reference_vectors)
    #     rest = self.population_size % len(self.reference_vectors) #iremos añadiendo el resto por orden de vector referencia
    #     groups = self.get_groups_reference_vectors(self.reference_vectors, k, rest)
    #     front = []
    #     for key, value in groups.items():
    #         front.extend(value)
    #     return front
    
    # def get_groups_reference_vectors(self, vectors, k, rest = 0): #k es los k mejores de cada uno, y rest por si sobran
    #     calculate_distances_to_reference_vectors(self.population, vectors)
    #     groups = {}
    #     for reference_vector in vectors:
    #         sorted_population = sorted(self.population, key=lambda ind: ind.vector_distance[reference_vector], reverse=True)
    #         if rest > 0:
    #             groups[reference_vector] = sorted_population[:k + 1]
    #             rest -= 1
    #         else:
    #             groups[reference_vector] = sorted_population[:k]
    #     return groups
    
    #------------------------
    #-------REFLECTION-------
    #------------------------

    def update_reflection(self, clusters):
        clusters_reflection = []
        for cluster, info in clusters.items():
            system_prompt, user_prompt = self.Reader.get_cluster_reflection_prompt(info, self.of)
            ref = self.LLMManager.get_reflection(system_prompt, user_prompt)
            clusters_reflection.append({'Centroid': info['Centroid'], 'Reflection': ref})
        system_promptI, user_promptI = self.Reader.get_long_reflectionI_prompt(self.long_reflectionI, clusters_reflection, self.of)
        system_promptII, user_promptII = self.Reader.get_long_reflectionII_prompt(self.long_reflectionI, clusters_reflection, self.of)
        self.long_reflectionI = self.LLMManager.get_reflection(system_promptI, user_promptI)
        self.long_reflectionII = self.LLMManager.get_reflection(system_promptII, user_promptII)

        self.save_reflections()

    def get_k_means(self, population):
        evaluations = np.array([list(ind.evaluation.values()) for ind in population])
        k = self.select_best_k(evaluations, population)
        self.ks.append(k)
        kmeans = KMeans(n_clusters=k, random_state=42)
        kmeans.fit(evaluations)
        clusters = {label:{'Individuals': [], 'Centroid': centroid} for label, centroid in enumerate(kmeans.cluster_centers_)} #guardamos centroide y individuo para cada cluster
        for ind, label in zip(population, kmeans.labels_):
            clusters[label]['Individuals'].append(ind)
        return clusters
    
    def select_best_k(self, evaluations, population): #Método de silueta
        silhouette_scores = []
        max_k = len(population) // 2
        if max_k <= 2:
            return max_k
        range_k = range(2, max_k + 1)

        for k in range_k:
            kmeans = KMeans(n_clusters=k, random_state=42)
            kmeans.fit(evaluations)
            score = silhouette_score(evaluations, kmeans.labels_)
            silhouette_scores.append(score)

        best_k = range_k[np.argmax(silhouette_scores)]
        print(f'K selected: ', best_k)
        return best_k

    #--------------------------------
    #-----CROSSOVER AND MUTATION-----
    #--------------------------------

    def crossover(self, parents): #sólo un crossover guiado por long_reflection entre dos padres

        self.update_crossover_probabilities()
        sons = []
        crossover_length = len(parents) - round(len(parents) * self.mutation_prob)
        explorative_length = round(crossover_length * self.explorative_prob)
        intense_length = crossover_length - explorative_length

        for i in range(intense_length):
            parent1 = self.tournament_selection_nsgaII(parents)
            parents_without_parent1 = list(filter(lambda p: p != parent1, parents))
            parent2 = self.tournament_selection_nsgaII(parents_without_parent1) #seleccionamos población sin parent2
            sCrossover_prompt, uCrossover_prompt = self.Reader.get_crossoverI_prompt(self.long_reflectionI, parent1, parent2)
            son = self.create_individual(sCrossover_prompt, uCrossover_prompt)
            sons.append(son)

        for i in range(explorative_length):
            parent1 = self.tournament_selection_nsgaII(parents)
            parents_without_parent1 = list(filter(lambda p: p != parent1, parents))
            parent2 = self.tournament_selection_nsgaII(parents_without_parent1) #seleccionamos población sin parent2
            sCrossover_prompt, uCrossover_prompt = self.Reader.get_crossoverII_prompt(self.long_reflectionII, parent1, parent2)
            son = self.create_individual(sCrossover_prompt, uCrossover_prompt)
            sons.append(son)

        return sons
    
    def elitist_mutation(self, parents): #sólo una especie de mutación cogiendo los mejores individuos del frente pareto
        best_score = float('-inf')
        for individual in parents:
            if individual.evaluation['Mean'] > best_score:
                best_score = individual.evaluation['Mean']
                best_individual = individual
        sons = []
        mutation_length = round(len(parents) * self.mutation_prob)
        for i in range(mutation_length):
            sMutation_prompt, uMutation_prompt = self.Reader.get_mutation_prompt(self.long_reflectionI, best_individual)
            son = self.create_individual(sMutation_prompt, uMutation_prompt)
            sons.append(son)
        return sons
    
    def tournament_selection_nsgaII(self, parents):
        if len(parents) == 1:
            return random.sample(parents, 1)
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
            
    def update_crossover_probabilities(self):
        factor = 1 / (1 + np.exp(self.a * ((self.iteration / self.max_evolutions) - self.b)))
        self.intense_prob = self.intense_prob_init + (self.intense_prob_end - self.intense_prob_init) * (1 - factor)
        self.explorative_prob = 1 - self.intense_prob

    #--------------------------
    #----EVOLUTION FUNCTION----
    #--------------------------

    def start(self):

        start_time = time.time()
        self.init_population()

        while self.iteration < self.max_evolutions:

            print(f'Starting evolution {self.iteration}...')
            self.evaluate_population()
            print(f'Evaluated.')

            if len(self.population) == 0:
                print('No hay ningún heurístico válido.')
                return
            
            parents, rest = self.select_parents_II()
            print(f'Selected.')
            self.whole_population.extend(rest)

            clusters = self.get_k_means(parents)
            self.update_reflection(clusters)
            print(f'Reflected.')

            crossover_sons = self.crossover(parents)
            print(f'Crossover done.')

            mutation_sons = self.elitist_mutation(parents)
            print(f'Mutation done.')

            parents.extend(crossover_sons)
            parents.extend(mutation_sons)

            self.population = parents

            self.iteration += 1

        self.evaluate_population()
        self.whole_population.extend(parents)
        
        end_time = time.time()

        self.save_final_information(end_time - start_time)
    
    #---------------------------
    #-----EXECUTION FOLDER -----
    #---------------------------

    def create_execution_folder(self):

        os.makedirs(self.folder_path)
        os.makedirs(self.folder_path+'/heuristics')

        heuristics_data_path = os.path.join(self.folder_path, "heuristics_data.json")
        parameters_path = os.path.join(self.folder_path, "parameters.json")

        with open(heuristics_data_path, 'w') as archivo_json:
                json.dump([], archivo_json, indent=4)

        parameters = {'population size': self.population_size,
                      'problem name': self.problem_name,
                      'max evolutions': self.max_evolutions,
                      'a': self.a,
                      'b': self.b,
                      'explorative initial probability': self.explorative_prob_init,
                      'intense initial probability': self.intense_prob_init,
                      'mutation': self.mutation_prob}
        
        with open(parameters_path, 'w') as archivo_json:
                json.dump(parameters, archivo_json, indent=4)

    def save_final_information(self, time):

        finish_path = os.path.join(self.folder_path, "final_information.json")
            
        finish_information = {'total heuristics': self.total_heuristics,
                      'correct heuristics': self.correct_heuristics,
                      'incorrect heuristics': self.incorrect_heuristics,
                      'infeasible heuristics': self.infeasible_heuristics,
                      'repaired heuristics': self.repaired_heuristics,
                      'time': time,
                      'total petitions': self.LLMManager.LLMClient.total_petitions,
                      'total input tokens': self.LLMManager.LLMClient.total_input_tokens,
                      'total output tokens': self.LLMManager.LLMClient.total_output_tokens,
                      'k': str(self.ks)}
        
        with open(finish_path, 'w') as archivo_json:
                json.dump(finish_information, archivo_json, indent=4)
    
    def save_reflections(self):
        
        with open(f'{self.folder_path}/long_reflectionI.txt', "a") as file:
            file.write(f'Reflection {self.iteration}: {self.long_reflectionI}')
        with open(f'{self.folder_path}/long_reflectionII.txt', "a") as file:
            file.write(f'Reflection {self.iteration}: {self.long_reflectionII}')

    #--------------------------
    #-----ABSTRACT METHODS-----
    #--------------------------

    @abstractmethod
    def feasibility(self, instance, solution): #returns True if it is feasible, infeasibility information if it is not.
        pass

    @abstractmethod
    def objective_functions(self, data, solution): #return a dictionary with key: name of the objective function, value: fitness in the objective function
        pass

    @abstractmethod
    def decode_instance(self, individual): #return a dictionary with key: name of the objective function, value: fitness in the objective function
        pass