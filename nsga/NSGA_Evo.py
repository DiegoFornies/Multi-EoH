from abc import ABC, abstractmethod
from prompts import PromptManager
from llm import LLMManager

class NSGA_Evo(ABC):
    def __init__(self, problem_path, population_size):
        self.problem_path = problem_path
        self.promptManager = PromptManager(problem_path = problem_path)
        self.population_size = population_size
        self.population = []
        self.LLMManager = LLMManager()

    def init_population(self):
        for n in range(self.population_size):
            system_prompt, user_prompt = self.promptManager.get_initialization_prompt()
            description, code = self.create_individual(system_prompt, user_prompt)
            self.population.append({'Description' : description, 'Code': code, 'Evaluation': {}})

    def create_individual(self, system_prompt, user_prompt):
        encoded_ind = llm.ask(system_prompt, user_prompt)
        description, code = self.LLMManager.get_heuristic(system_prompt, user_prompt)
        return (description, code)
    
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