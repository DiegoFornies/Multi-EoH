import traceback
import json
import threading
import ctypes
import numpy as np
import math

class Individual:
    def __init__(self, code, reader, llmmanager, folder_path, id, iteration):

        self.id = id #id único para cada individuo

        self.code = code  #Código del individuo (su heurística)

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

        self.max_time = 120

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
                        self.repair(str(t))
                    self.repair_counter += 1
                    evaluation = 'Time Out Error'
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
        print(message)
        system_prompt, user_prompt = self.Reader.get_repair_prompt(self.code, message)
        self.code = self.LLMManager.get_heuristic(system_prompt, user_prompt)
        return ''
    
    def get_solutions(self, instances):
        solutions = {}
        for inst_name, inst_value in instances.items():
            resultado = [None]
            excepcion = [None]

            local_vars = {}
            exec(self.code, globals(), local_vars)
            heuristic = local_vars['heuristic']

            def run_heuristic():
                try:
                    resultado[0] = heuristic(inst_value)
                except Exception as e:
                    excepcion[0] = e

            hilo = threading.Thread(target=run_heuristic)
            hilo.start()
            hilo.join(self.max_time)

            if hilo.is_alive():
                ctypes.pythonapi.PyThreadState_SetAsyncExc(
                    ctypes.c_long(hilo.ident), ctypes.py_object(SystemExit)
                )
                hilo.join(0.1)

                if hilo.is_alive():
                    raise TimeoutError

            if excepcion[0]:
                raise excepcion[0]
            
            solutions[inst_name] = resultado[0]
            
        del local_vars['heuristic']

        return solutions
    
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