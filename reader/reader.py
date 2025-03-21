import os

class Reader:
    def __init__(self, problem_name, prompt_path='prompts'):
        """Inicializa el gestor de prompts con la ruta base y el problema a cargar."""
        self.prompt_path = prompt_path
        self.problem_path = 'problems/' + problem_name
        self.reflection_path = prompt_path + '/reflection'
        self.n_role = 0
        self.n_heuristic_seed = 0
        self.cache = {}  #Diccionario para cachear prompts ya leídos

    def read_file(self, path):
        """Lee el contenido de un archivo de texto con cacheo."""
        if path in self.cache:
            return self.cache[path]

        try:
            with open(path, 'r') as f:
                content = f.read()
                self.cache[path] = content
                return content
        except FileNotFoundError:
            print(f"El archivo '{path}' no fue encontrado.")
            return ""
        
    def get_system_generator_prompt(self):
        prompt = self.read_file(f'{self.prompt_path}/system_generator_prompt.txt')
        role_init = self.get_role()
        return prompt.replace('{role_init}', role_init)

    def get_task_description(self):
        task_description = self.read_file(f'{self.prompt_path}/task_description.txt')
        role_init = self.get_role()
        problem_description = self.read_file(f'{self.problem_path}/problem_description.txt')
        function_description = self.read_file(f'{self.problem_path}/function_description.txt')
        return task_description.replace('{role_init}', role_init).replace('{problem_description}', problem_description).replace('{function_description}', function_description)

    def get_initialization_prompt(self):
        user_prompt = self.read_file(f'{self.prompt_path}/user_population_initialization.txt')
        task_description = self.get_task_description()
        seed_function = self.read_file(f'{self.problem_path}/seed_function.txt')
        return self.get_system_generator_prompt(), user_prompt.replace('{task_description}', task_description).replace('{seed_function}', seed_function)
    
    def get_role(self):
        """Retorna el role y actualiza su número"""
        roles = self.read_file(f'{self.prompt_path}/role_init.txt').split('\n')
        role = roles[self.n_role]
        if self.n_role == len(roles) - 1:
            self.n_role = 0
        else:
            self.n_role += 1
        return role
    
    def get_heuristic_seed(self):
        """Retorna el role y actualiza su número"""
        seeds = self.read_file(f'{self.problem_path}/heuristic_seeds.txt').split('\n')
        seed = seeds[self.n_heuristic_seed]
        if self.n_heuristic_seed == len(seeds) - 1:
            self.n_heuristic_seed = 0
        else:
            self.n_heuristic_seed += 1
        return seed
    
    def get_instances(self):
        instances = {}
        for filename in os.listdir(f'{self.problem_path}/instances/'):
            if filename.endswith('.txt'):
                content = self.read_file(f'{self.problem_path}/instances/{filename}')
                instances[filename] = content

        return instances

    def get_cluster_reflection_prompt(self, cluster, of):
        system_prompt = self.read_file(f'{self.reflection_path}/system_short_reflection.txt')
        user_prompt = self.read_file(f'{self.reflection_path}/user_short_reflection.txt')
        centroid = cluster['Centroid']
        individuals = cluster['Individuals']

        individuals_info = ''
        for individual in individuals:
            individuals_info += f'Heuristic {individual.id}: \nDescription: {individual.description} \nCode: {individual.code}\n'

        performance = ''

        for num, (of_name, _) in enumerate(of.items()):
            performance += f'{of_name}: {centroid[num]}     '
        user_prompt = user_prompt.replace('{cluster_performance}', performance).replace('{heuristics}', individuals_info)
        return system_prompt, user_prompt
    
    def get_long_reflection_prompt(self, long_reflections, clusters, of):
        system_prompt = self.read_file(f'{self.reflection_path}/system_long_reflection.txt')
        user_prompt = self.read_file(f'{self.reflection_path}/user_long_reflection.txt')

        clusters_reflections = ''
        for cluster in clusters:
            centroid = cluster['Centroid']
            performance = ''
            for num, (of_name, _) in enumerate(of.items()):
                performance += f'{of_name}: {centroid[num]}     '
            reflection = cluster['Reflection']
            clusters_reflections += f'Cluster general performance: {performance}\nCluster reflection: {reflection}\n'
        user_prompt = user_prompt.replace('{clusters_reflections}', performance).replace('{long_reflections}', long_reflections)
        return system_prompt, user_prompt
    
    def get_repair_prompt(self, broken_function, error):
        system_prompt = self.read_file(f'{self.prompt_path}/system_repair_prompt.txt')
        user_prompt = self.read_file(f'{self.prompt_path}/user_repair_prompt.txt')

        problem_description = self.read_file(f'{self.problem_path}/problem_description.txt')
        function_description = self.read_file(f'{self.problem_path}/function_description.txt')

        user_prompt = user_prompt.replace('{broken_function}', broken_function).replace('{problem_description}', problem_description).replace('{function_description}',function_description).replace('{error}', error)
        return system_prompt, user_prompt
    
    def get_crossover_prompt(self, long_reflection, parent1, parent2):
        role_init = self.get_role()
        system_prompt = self.read_file(f'{self.prompt_path}/system_generator_prompt.txt').replace('{long_reflection}', long_reflection).replace('{role_init}', role_init)
        user_prompt = self.read_file(f'{self.prompt_path}/user_crossover_prompt.txt')
        task_description = self.get_task_description()

        user_prompt = user_prompt.replace('{task_description}', task_description).replace('{parent1}', parent1.code).replace('{parent2}', parent2.code)
        return system_prompt, user_prompt
    
    def get_mutation_prompt(self, long_reflection, parent):
        role_init = self.get_role()
        system_prompt = self.read_file(f'{self.prompt_path}/system_generator_prompt.txt').replace('{role_init}', role_init)
        user_prompt = self.read_file(f'{self.prompt_path}/user_mutation_prompt.txt')
        task_description = self.get_task_description()

        user_prompt = user_prompt.replace('{task_description}', task_description).replace('{parent}', parent.code).replace('{long_reflection}', long_reflection)
        return system_prompt, user_prompt