import traceback
import json
import threading
import ctypes
import numpy as np
import math
import re

class Individual:
    def __init__(self, code, reader, llmmanager, folder_path, id, iteration):

        self.id = id #id único para cada individuo

        self.max_time = 100

        self.code = code  #Código del individuo (su heurística)
        self.timeout_code = self.get_timeout_code()

        self.base_evaluation = None
        self.normalized_evaluation = None  #Evaluación del individuo completa
        self.evaluation = None #Evaluación del individuo mediada y normalizada
        self.evaluated = False

        self.valid = False
        self.max_repair = 1
        self.repair_counter = 0

        self.iteration_creation = iteration

        self.front = None
        self.crowding_distance = None
        self.vector_distance = {}

        self.Reader = reader
        self.LLMManager = llmmanager

        self.folder_path = folder_path

        self.code_file = f'{self.folder_path}/heuristics/heuristic{self.id}.py'
        with open(self.code_file, 'w') as file:
            file.write(self.code)

    def evaluate(self, instances, objective_functions, feasibility, of): #devuelve false si infeasible
        if not self.evaluated:
            while not self.valid and self.repair_counter <= self.max_repair:
                evaluation = {}
                try:
                    solutions = self.get_solutions(instances)
                    for instance_name, solution in solutions.items():
                        f = feasibility(instances[instance_name], solution)
                        if f == True:
                            self.valid = True
                            results = objective_functions(instances[instance_name], solution)
                            evaluation[instance_name] = {}
                            for of_name, _ in of.items():
                                evaluation[instance_name][of_name] = results[of_name]
                        else:
                            if self.repair_counter < self.max_repair:
                                self.repair(f)
                            self.repair_counter += 1
                            evaluation = 'Infeasible'
                            self.valid = False
                            break
                except TimeoutError as t:
                    if self.repair_counter < self.max_repair:
                        self.repair('The heuristic takes too long in executing. Please, check for infinite loops and solve it.')
                    self.repair_counter += 1
                    evaluation = 'Code Error'
                    self.valid = False
                except Exception as e:
                    if self.repair_counter < self.max_repair:
                        self.repair(traceback.format_exc())
                    self.repair_counter += 1
                    evaluation = 'Code Error'
                    self.valid = False
            self.base_evaluation = evaluation

            #guardamos información del heurístico en un json

            with open(f'{self.folder_path}/heuristics_data.json', 'r') as archivo_json:
                datos = json.load(archivo_json)

            datos.append(self.to_dict())

            with open(f'{self.folder_path}/heuristics_data.json', 'w') as archivo_json:
                json.dump(datos, archivo_json, indent=4)

    def repair(self, message):
        print(f'Error message: {message}')
        system_prompt, user_prompt = self.Reader.get_repair_prompt(self.code, message)
        self.code = self.LLMManager.get_heuristic(system_prompt, user_prompt)
        return ''
    
    def get_solutions(self, instances):
        solutions = {}
        for inst_name, inst_value in instances.items():

            local_vars = {}
            exec(self.timeout_code, globals(), local_vars)
            heuristic = local_vars['heuristic']
            resultado = heuristic(inst_value)
            solutions[inst_name] = resultado
            
        del local_vars['heuristic']

        return solutions
    
    def get_timeout_code(self):
        while_pattern = r'^\s*(while|for)\s+.*\s*:$'
        def_pattern = r'^\s*def\s+heuristic\s*\(.*\)\s*:'

        code_splitted = self.code.split('\n')

        new_code = []

        for i, content in enumerate(code_splitted):
            new_code.append(content)
            if re.match(def_pattern, content):
                if i < len(code_splitted) - 1:
                    next_line = code_splitted[i + 1]
                    indentation_count = len(next_line) - len(next_line.lstrip(' '))
                    indent = ' ' * indentation_count
                    new_line = f'{indent}import time as waytomeasuretime\n{indent}waytomeasuretimestart = waytomeasuretime.time()'
                    new_code.append(new_line)

            elif re.match(while_pattern, content):
                if i < len(code_splitted) - 1:
                    next_line = code_splitted[i + 1]
                    indentation_count = len(next_line) - len(next_line.lstrip(' '))
                    indent = ' ' * indentation_count
                    new_line = f'{indent}if waytomeasuretime.time() - waytomeasuretimestart > {self.max_time}:\n{indent}     raise TimeoutError'
                    new_code.append(new_line)

        return '\n'.join(new_code)
    
    def average(self, of, num_instances):
        if not self.evaluated:
            if self.valid:
                global_sum = 0
                mean_evaluation = {}
                for of_name, _ in of.items():
                    sum = 0
                    for inst_name, inst_ev in self.normalized_evaluation.items():
                        sum += inst_ev[of_name]
                    mean_evaluation[of_name] = sum / num_instances
                    global_sum += mean_evaluation[of_name]
                
                mean_evaluation['Mean'] = global_sum / len(of) #media global
                self.evaluation = mean_evaluation
    
    def get_dominance(self, of, population):
        if self.valid:
            dominated = False
            for individual in population:
                if not individual.id == self.id and self.is_dominated(of, individual):  # Si ind1 es dominado por ind2
                    dominated = True
                    break
            return dominated
        return True # si no es valido, devolvemos que es dominada

    def is_dominated(self, of, ind):
        dominated = False
        for of_name, _ in of.items():
            if self.evaluation[of_name] > ind.evaluation[of_name]:
                return False
            if self.evaluation[of_name] < ind.evaluation[of_name]:
                dominated = True
        return dominated
    
    def to_dict(self):
        individual = {'id': self.id,
                      'code file': self.code_file,
                      'valid': self.valid,
                      'generation': self.iteration_creation,
                      'repair counter': self.repair_counter,
                      'evaluation': self.base_evaluation}
        return individual