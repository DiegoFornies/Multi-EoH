import random
import traceback
import copy
import json

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
                        print(f'Checking feasibility of individual {self.id} in instance {instance_name}')
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
        local_vars = {}
        exec(self.code, globals(), local_vars)
        heuristic = local_vars['heuristic']
        solutions = {}
        for name, instance in instances.items():
            print(f'Getting solution of instance {name}')
            solutions[name] = heuristic(instance)
        del local_vars['heuristic']
        return solutions
    
    def normalize(self, of):
        self.normalized_evaluation = copy.deepcopy(self.base_evaluation)
        for of_name, of_info in of.items():
            for inst_name, inst_ev in self.normalized_evaluation.items():
                min = of_info['min_score'][inst_name]
                max = of_info['max_score'][inst_name]
                divisor = max - min
                if divisor == 0:
                    divisor = 1 #solo se cumple si todos tienen el mismo fitness
                value = (max - inst_ev[of_name]) / divisor
                if of_info['Objective'] == 'Maximize':
                    value = 1 - value
                self.normalized_evaluation[inst_name][of_name] = value

    def average(self, of, num_instances):
        if not self.evaluated:
            if self.valid:
                global_sum = 0
                mean_evaluation = {}
                for of_name, of_info in of.items():
                    sum = 0
                    for inst_name, inst_ev in self.normalized_evaluation.items():
                        sum += inst_ev[of_name]
                    mean_evaluation[of_name] = sum / num_instances
                    global_sum += mean_evaluation[of_name]
                
                mean_evaluation['Mean'] = global_sum / len(of) #media global
                self.evaluation = mean_evaluation

    def update_minmax(self, of):
        if not self.evaluated:
            if self.valid:
                for of_name, of_info in of.items():
                    for inst_name, inst_ev in self.base_evaluation.items():
                        if of_info['min_score'][inst_name] > inst_ev[of_name]:
                            of_info['min_score'][inst_name] = inst_ev[of_name]
                        if of_info['max_score'][inst_name] < inst_ev[of_name]:
                            of_info['max_score'][inst_name] = inst_ev[of_name]
        return of
    
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