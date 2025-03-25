
def heuristic(input_data):
    """
    A heuristic for the FJSSP that prioritizes machines with the earliest available time and short processing times.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']
    
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {job: 0 for job in jobs}
    schedule = {job: [] for job in jobs}
    
    operations = []
    for job, ops in jobs.items():
        for op_idx, (machines, times) in enumerate(ops):
            operations.append((job, op_idx, machines, times))

    #sort the operations
    operations.sort(key=lambda x: (x[0], x[1])) 
            
    while operations:
        best_op = None
        best_machine = None
        earliest_start = float('inf')
        
        for job, op_idx, machines, times in operations:
            available_machines = []
            for i in range(len(machines)):
                available_machines.append((machines[i],times[i]))

            
            for machine,time in available_machines:
                start_time = max(machine_available_time[machine], job_completion_time[job])
                if start_time < earliest_start:
                    earliest_start = start_time
                    best_op = (job, op_idx, machines, times)
                    best_machine = (machine,time)
                    
        
        job, op_idx, machines, times = best_op
        machine,time = best_machine
        start_time = max(machine_available_time[machine], job_completion_time[job])
        end_time = start_time + time
        
        schedule[job].append({
            'Operation': op_idx + 1,
            'Assigned Machine': machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': time
        })
        
        machine_available_time[machine] = end_time
        job_completion_time[job] = end_time
        
        operations.remove(best_op)
    
    return schedule
