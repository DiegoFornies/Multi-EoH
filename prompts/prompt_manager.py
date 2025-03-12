import os

class PromptManager:
    def __init__(self, problem_path, base_path='prompts/'):
        """Inicializa el gestor de prompts con la ruta base y el problema a cargar."""
        self.base_path = base_path
        self.problem_path = problem_path
        self.n_role = 0
        self.n_heuristic_seed = 0
        self.cache = {}  #Diccionario para cachear prompts ya leídos

    def read_prompt(self, path):
        """Lee el contenido de un archivo de texto con cacheo."""
        if path in self.cache:
            return self.cache[path]

        full_path = os.path.join(self.base_path, path)
        try:
            with open(full_path, 'r') as f:
                content = f.read()
                self.cache[path] = content
                return content
        except FileNotFoundError:
            print(f"El archivo '{full_path}' no fue encontrado.")
            return ""

    def read_problem_specifications(self):
        """Lee y devuelve las especificaciones del problema desde archivos con cacheo."""
        return (
            self.read_prompt(f'{self.problem_path}/problem_description.txt'),
            self.read_prompt(f'{self.problem_path}/input_specifications.txt'),
            self.read_prompt(f'{self.problem_path}/output_specifications.txt')
        )

    def user_initialization_prompt(self):
        """Genera el prompt de inicialización del usuario con los datos del problema."""
        problem_description, input_specifications, output_specifications = self.read_problem_specifications()
        
        prompt = self.read_prompt('user_population_initialization.txt')
        return (prompt
                .replace("{problem_description}", problem_description)
                .replace("{input_specifications}", input_specifications)
                .replace("{heuristic_seed}", self.get_heuristic_seed())
                .replace("{output_specifications}", output_specifications))

    def system_initialization_prompt(self):
        """Genera el prompt de inicialización del sistema según el rol."""    
        prompt = self.read_prompt('system_population_initialization.txt')
        return prompt.replace("{role_init}", self.get_role())

    def get_initialization_prompt(self):
        """Retorna el prompt de inicialización para el sistema y el usuario."""
        return self.system_initialization_prompt(), self.user_initialization_prompt()
    
    def get_role(self):
        """Retorna el role y actualiza su número"""
        roles = self.read_prompt('role_init.txt').split('\n')
        role = roles[self.n_role]
        if self.n_role == len(roles) - 1:
            self.n_role = 0
        else:
            self.n_role += 1
        return role
    
    def get_heuristic_seed(self):
        """Retorna el role y actualiza su número"""
        seeds = self.read_prompt(f'{self.problem_path}/heuristic_seeds.txt').split('\n')
        seed = seeds[self.n_heuristic_seed]
        if self.n_heuristic_seed == len(seeds) - 1:
            self.n_heuristic_seed = 0
        else:
            self.n_heuristic_seed += 1
        return seed
    
    def get_instances(self):
        instances = []
        for filename in os.listdir(f'{self.problem_path}/instances/'):
            if filename.endswith('.txt'):
                content = self.read_prompt('{self.problem_path}/instances/{filename}')
                instances.append(content)     

        return instances
