
def heuristic(input_data):
    """
    A heuristic for FJSSP that considers machine load balancing and
    operation processing times to minimize makespan.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {job: [] for job in jobs}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {job: 0 for job in jobs}

    operations = []
    for job, op_list in jobs.items():
        for op_idx, (machines, times) in enumerate(op_list):
            operations.append({
                'job': job,
                'op_idx': op_idx,
                'machines': machines,
                'times': times
            })
    
    # Sort operations based on shortest processing time first
    operations.sort(key=lambda op: min(op['times']))
    

    for operation in operations:
        job = operation['job']
        op_idx = operation['op_idx']
        machines = operation['machines']
        times = operation['times']

        best_machine = None
        min_end_time = float('inf')

        for i, machine in enumerate(machines):
            processing_time = times[i]
            start_time = max(machine_available_time[machine], job_completion_time[job])
            end_time = start_time + processing_time

            if end_time < min_end_time:
                min_end_time = end_time
                best_machine = machine
                best_start_time = start_time
                best_processing_time = processing_time
                
        
        schedule[job].append({
            'Operation': op_idx + 1,
            'Assigned Machine': best_machine,
            'Start Time': best_start_time,
            'End Time': best_start_time + best_processing_time,
            'Processing Time': best_processing_time
        })
            
        machine_available_time[best_machine] = best_start_time + best_processing_time
        job_completion_time[job] = best_start_time + best_processing_time
        

    return schedule
