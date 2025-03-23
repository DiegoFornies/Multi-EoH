import numpy as np
from collections import defaultdict

def objective_functions(data, solution):

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