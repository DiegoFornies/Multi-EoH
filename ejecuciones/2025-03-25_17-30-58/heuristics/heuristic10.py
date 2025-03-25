
def heuristic(input_data):
    """
    Schedules jobs by prioritizing operations with fewer machine options,
    and assigning them to the machine with the earliest available time.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}
    
    operations = []
    for job_id, job_ops in jobs.items():
        for op_idx, op_data in enumerate(job_ops):
            operations.append((len(op_data[0]), job_id, op_idx, op_data))  # (num_machines, job_id, op_index, op_data)
    
    operations.sort() # Sort by number of feasible machines

    for _, job_id, op_idx, op_data in operations:
        machines, times = op_data
        op_num = op_idx + 1
        
        best_machine = None
        best_start_time = float('inf')
        best_processing_time = None

        for i in range(len(machines)):
            machine = machines[i]
            processing_time = times[i]
            
            start_time = max(machine_available_times[machine], job_completion_times[job_id])
            
            if start_time < best_start_time:
                best_start_time = start_time
                best_machine = machine
                best_processing_time = processing_time
        
        end_time = best_start_time + best_processing_time
        
        if job_id not in schedule:
            schedule[job_id] = []
        
        schedule[job_id].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': best_start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })

        machine_available_times[best_machine] = end_time
        job_completion_times[job_id] = end_time
    
    return schedule
