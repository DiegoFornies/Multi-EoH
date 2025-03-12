from abc import ABC, abstractmethod
from prompts import prompt_reader as pr
import llm
import re

class NSGA_Evo(ABC):
    def __init__(self, problem_path, population_size):
        self.problem_path = problem_path
        self.promptManager = pr.PromptManager(problem_path = problem_path)
        self.population = []
        self.population_size = population_size

    def init_population(self):
        for n in range(self.population_size):
            system_prompt, user_prompt = self.promptManager.get_initialization_prompt()
            description, code = self.create_individual(system_prompt, user_prompt)
            self.population.append({'Description' : description, 'Code': code, 'Evaluation': {}})

    def create_individual(self, system_prompt, user_prompt):
        encoded_ind = llm.ask(system_prompt, user_prompt)
        description, code = self.decoded_individual(encoded_ind)
        return (description, code)
    
    def decode_individual(self, encode_ind):
        code_pattern = r'```python(.*?)```'
        code_matches = re.findall(code_pattern, encode_ind, re.DOTALL)
        description = re.sub(code_pattern, '', encode_ind).strip()
        
        return description, code_matches
    
    def evaluate_population(self):
        for individual in self.population:
            evaluation = self.evaluate_individual(individual)
            individual['Evaluation'] = evaluation

    @abstractmethod
    def evaluate_individual(self): #return a dictionary of objective function values
        pass

    @abstractmethod
    def get_individual_solution(self, individual):
        pass

    
class NSGA_Evo_JSSP(NSGA_Evo):
    def __init__(self, problem_path, population_size):
        super().__init__(problem_path, population_size)
        self.instances = self.get_instances()

    def get_instances(self):
        instances = self.promptManager.get_instances()
        decoded_ins = []
        for instance in instances:
            decoded_ins.append(self.decode_instances(instance))
        return decoded_ins
    
    def decode_instances(self, instance):
        lines = instance.strip().split('\n')
        
        first_line = lines[0].strip().split()
        num_jobs = int(first_line[0])
        num_machines = int(first_line[1])
        
        jobs = {}
        line_index = 1
        
        for job_id in range(1, num_jobs + 1):
            job_info = lines[line_index].strip().split()
            num_operations = int(job_info[0])
            operations = []
            
            index = 1
            for _ in range(num_operations):
                num_machines_for_op = int(job_info[index])
                index += 1
                machines_list = []
                times_list = []
                
                for _ in range(num_machines_for_op):
                    machine_id = int(job_info[index])
                    processing_time = int(job_info[index + 1])
                    machines_list.append(machine_id)
                    times_list.append(processing_time)
                    index += 2
                
                operations.append((machines_list, times_list))
            
            jobs[job_id] = operations
            line_index += 1
        return {'n_jobs': num_jobs, 'n_machines': num_machines, 'jobs': jobs}
    
    def evaluate_individual(self, individual):
        solutions = self.get_individual_solution(individual)
        instances = self.instances
        for i, solution in enumerate(solutions):
            makespan = self.calculate_makespan(instances[i], solution)

    def get_individual_solution(self, individual):
        code = individual['Code']
        exec(code)
        solutions = []
        for instance in self.instances:
            solutions.append(heuristic(instance)) #heurístico del individuo, nombre de la función 'heuristic'
        return solutions
    
    def calculate_makespan(self, instance, solution):
        makespan = 0
        for _, operations in solution.items():
            for operation in operations:
                end_time = operation['End Time']
                makespan = max(makespan, end_time)
        return makespan


nsga = NSGA_Evo('jssp', 10)
nsga.init_population()
print(nsga.population)