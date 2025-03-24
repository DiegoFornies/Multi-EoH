
def heuristic(input_data):
    """
    Heuristic for FJSSP scheduling. Prioritizes shortest processing time
    and earliest available machine for each operation.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']
    
    schedule = {job: [] for job in range(1, n_jobs + 1)}
    machine_available_time = {machine: 0 for machine in range(1, n_machines + 1)}
    job_completion_time = {job: 0 for job in range(1, n_jobs + 1)}
    
    operations = []
    for job, operations_list in jobs_data.items():
        for op_idx, operation in enumerate(operations_list):
            operations.append((job, op_idx + 1, operation))
    
    # Sort operations based on shortest processing time
    operations.sort(key=lambda x: min(x[2][1]))
    
    for job, op_num, operation_data in operations:
        machines, times = operation_data
        
        best_machine, best_time = None, float('inf')
        earliest_start = float('inf')
        
        for i, machine in enumerate(machines):
            time = times[i]
            start_time = max(machine_available_time[machine], job_completion_time[job])
            
            if start_time < earliest_start:
                earliest_start = start_time
                best_machine = machine
                best_time = time
                
        start_time = max(machine_available_time[best_machine], job_completion_time[job])
        end_time = start_time + best_time
        
        schedule[job].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_time
        })
        
        machine_available_time[best_machine] = end_time
        job_completion_time[job] = end_time
        
    return schedule
