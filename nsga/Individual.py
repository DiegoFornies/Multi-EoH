import random

class Individual:
    _counter = 0
    def __init__(self, description, code):
        self.id = Individual._counter #id único para cada individuo
        Individual._counter += 1
        self.description = description  #Descripción del individuo
        self.code = code  #Código del individuo (su heurística)
        self.evaluation = None  #Evaluación del individuo (un diccionario de valores de las funciones objetivo)
        self.crowding_distance = 0.0
        self.vector_distance = {}
        self.feasible = False
        self.max_repair = 3

    def evaluate(self, instances, objective_functions, feasibility, of): #devuelve false si infeasible
        if self.evaluation == None:
            solutions = self.get_solutions(instances)
            evaluation = {}
            repair_counter = 0
            while not self.feasible and repair_counter <= self.max_repair:
                for instance_name, solution in solutions.items():
                    evaluation[instance_name] = {}
                    f = feasibility(instances[instance_name], solution)
                    if f == True:
                        self.feasible = True
                        results = objective_functions(solution)
                        for of_name, _ in of.items():
                            evaluation[instance_name][of_name] = results[of_name]
                    else:
                        print(self.code)
                        self.repair(f) #se manda el mensaje de por qué ha fallado
                        repair_counter += 1
                        break
            if self.feasible:
                self.evaluation = evaluation
                return True
            else:
                return False                

    def repair(self, message):
        #TODO modificar la descripción y el código, no devolver nada
        return ''

    def get_solutions(self, instances):
        local_vars = {}
        exec(self.code, globals(), local_vars)
        heuristic = local_vars['heuristic']
        solutions = {}
        for name, instance in instances.items():
            solutions[name] = heuristic(instance)
        del local_vars['heuristic']
        return solutions
    
    def normalize(self, of):
        if self.feasible:
            for of_name, of_info in of.items():
                for inst_name, inst_ev in self.evaluation.items():
                    min = of_info['min_score'][inst_name]
                    max = of_info['max_score'][inst_name]
                    divisor = max - min
                    if divisor == 0:
                        divisor = 1 #solo se cumple si todos tienen el mismo fitness
                    value = (max - inst_ev[of_name]) / divisor
                    if of_info['Objective'] == 'Maximize':
                        value = 1 - value
                    self.evaluation[inst_name][of_name] = value

    def average(self, of, num_instances):
        if self.feasible:
            mean_evaluation = {}
            for of_name, of_info in of.items():
                sum = 0
                for inst_name, inst_ev in self.evaluation.items():
                    sum += inst_ev[of_name]
                mean_evaluation[of_name] = sum / num_instances
            self.evaluation = mean_evaluation

    def update_minmax(self, of):
        if self.feasible:
            for of_name, of_info in of.items():
                for inst_name, inst_ev in self.evaluation.items():
                    if of_info['min_score'][inst_name] > inst_ev[of_name]:
                        of_info['min_score'][inst_name] = inst_ev[of_name]
                    if of_info['max_score'][inst_name] < inst_ev[of_name]:
                        of_info['max_score'][inst_name] = inst_ev[of_name]
        return of
    
    def get_dominance(self, of, population):
        if self.feasible:
            dominated = False
            for individual in population:
                if not individual.id == self.id and self.is_dominated(of, individual):  # Si ind1 es dominado por ind2
                    dominated = True
                    break
            return dominated
        return True # si no es feasible, devolvemos que es dominada

    def is_dominated(self, of, ind):
        dominated = False
        for of_name, _ in of.items():
            if self.evaluation[of_name] > ind.evaluation[of_name]:
                return False
            if self.evaluation[of_name] < ind.evaluation[of_name]:
                dominated = True
        return dominated