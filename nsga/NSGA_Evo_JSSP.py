from nsga import NSGA_Evo

#reference_vectors es una lista donde cada elemento es un vector en lista

class NSGA_Evo_JSSP(NSGA_Evo):
    
    def __init__(self, problem_name, initial_population, population_size, iterations, reflection, execution_name = '', reference_vectors = ''):
        objective_functions = {'Makespan': {'Objective': 'Minimize'}, 
                               'Separation': {'Objective': 'Minimize'}, #escribir el nombre que hay en objective_functions.py para cada una con su objetivo (minimizar o maximizar)
                               'Balance': {'Objective': 'Minimize'}}
        super().__init__(problem_name, initial_population, population_size, objective_functions, iterations, reflection, execution_name, reference_vectors)

    def feasibility(self, instance, solution):
        def operation_feasibility(): #operaciones empiezan de 0
            for job, operations in solution.items():
                job_operations = instance['jobs'][job]
                for op_idx, op in enumerate(operations):
                    assigned_machine = int(op['Assigned Machine'])
                    job_machine_list, job_processing_times = job_operations[op_idx]
                    if assigned_machine not in job_machine_list:
                        return False
                    assigned_processing_time = op['Processing Time']
                    if assigned_processing_time != job_processing_times[job_machine_list.index(assigned_machine)]:
                        return False
            return True

        def machine_feasibility(): #machine empieza de 0
            machine_operations = {int(machine): [] for machine in range(0, instance['n_machines'])}
            for job, operations in solution.items():
                for op in operations:
                    assigned_machine = int(op['Assigned Machine'])
                    start_time = op['Start Time']
                    end_time = op['End Time']
                    machine_op_list = machine_operations[assigned_machine]

                    for existing_op in machine_op_list:
                        if not (end_time <= existing_op['Start Time'] or start_time >= existing_op['End Time']):
                            return False
                    
                    machine_op_list.append({'Start Time': start_time, 'End Time': end_time})
                    machine_operations[assigned_machine] = machine_op_list

            return True

        def sequence_feasibility():
            for job, operations in solution.items():
                for op_idx in range(1, len(operations)):
                    prev_op_end_time = operations[op_idx - 1]['End Time']
                    curr_op_start_time = operations[op_idx]['Start Time']
                    if curr_op_start_time < prev_op_end_time:
                        return False
            return True
        
        def job_feasibility():
            if len(solution) != instance['n_jobs']:
                return False
            for job, operations in solution.items():
                if len(operations) != len(instance['jobs'][job]):
                    return False
            return True
        
        sorted_solution = {}
        
        for job in sorted(solution.keys()):
            sorted_solution[job] = sorted(solution[job], key=lambda op: op['Operation'])
        solution = sorted_solution
        message = ''
        if not machine_feasibility():
            message += '\nThe heuristic does not ensure machine feasibility, as it allows multiple operations on the same machine, which is not possible.'
        if not operation_feasibility():
            message += '\nThe heuristic does not ensure operation feasibility, as it assigns incorrect machines or processing times to operations.'
        if not sequence_feasibility():
            message += '\nThe heuristic does not ensure sequence feasibility, as some operations of the same job are performed simultaneously, or later operations are scheduled before earlier ones.'
        if not job_feasibility():
            message += '\nThe heuristic does not ensure job feasibility, as some operations or jobs are missing in the solution.'
        if message == '':
            return True
        return message

    def objective_functions(self, data, solution): #return a dictionary with key: name of the objective function, value: fitness in the objective function

        n_jobs = data['n_jobs']
        n_machines = data['n_machines']
        jobs = data['jobs']
        
        makespan = 0
        jobs_sep = 0
        machine_sat = [0] * n_machines
        
        for job in range(1, n_jobs + 1):
            single_job_sep = 0
            end_time = 0
            
            for operation in solution[job]:
                op_number = operation['Operation']
                assigned_machine = int(operation['Assigned Machine'])
                start_time = operation['Start Time']
                end_time_op = operation['End Time']
                processing_time = operation['Processing Time']
                
                machine_sat[assigned_machine] += processing_time
                
                if end_time > 0:
                    single_job_sep += (start_time - end_time)
                
                if end_time_op > makespan:
                    makespan = end_time_op
                    
                end_time = end_time_op
            
            jobs_sep += single_job_sep
        
        machine_sat = max(machine_sat)

        return {'Makespan': makespan, 'Separation': jobs_sep, 'Balance': machine_sat}

    def decode_instance(self, instance): #return the instance in the input format given to the LLM in the prompt
        
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