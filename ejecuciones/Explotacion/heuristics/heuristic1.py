
def heuristic(input_data):
    """A heuristic for the FJSSP that prioritizes operations with the shortest processing time and earliest machine availability."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    
    # Create a list of all operations, sorted by shortest processing time
    operations = []
    for job, operations_list in jobs_data.items():
        for op_idx, (machines, times) in enumerate(operations_list):
            operations.append((job, op_idx + 1, machines, times))
    
    operations.sort(key=lambda x: min(x[3])) # Sort by shortest processing time
    
    for job, op_num, machines, times in operations:
        best_machine = None
        min_end_time = float('inf')
        
        for i, machine in enumerate(machines):
            start_time = max(machine_available_time[machine], job_completion_time[job])
            end_time = start_time + times[i]
            
            if end_time < min_end_time:
                min_end_time = end_time
                best_machine = machine
                processing_time = times[i]
                start = start_time
            
        
        if job not in schedule:
            schedule[job] = []
        
        schedule[job].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start,
            'End Time': min_end_time,
            'Processing Time': processing_time
        })
        
        machine_available_time[best_machine] = min_end_time
        job_completion_time[job] = min_end_time
    
    return schedule
