
def heuristic(input_data):
    """A heuristic for FJSSP that considers machine availability and processing time."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']
    
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    
    schedule = {j: [] for j in range(1, n_jobs + 1)}
    
    operations = []
    for job_id, job_data in jobs.items():
        for op_idx, op_data in enumerate(job_data):
            operations.append((job_id, op_idx, op_data))
            
    # Sort operations based on shortest processing time
    operations.sort(key=lambda x: min(x[2][1]))

    for job_id, op_idx, op_data in operations:
        machines, times = op_data
        
        # Find the best machine for the current operation
        best_machine, min_end_time = -1, float('inf')
        for i in range(len(machines)):
            machine = machines[i]
            processing_time = times[i]
            
            start_time = max(machine_available_time[machine], job_completion_time[job_id])
            end_time = start_time + processing_time
            
            if end_time < min_end_time:
                min_end_time = end_time
                best_machine = machine
                best_processing_time = processing_time
        
        start_time = max(machine_available_time[best_machine], job_completion_time[job_id])
        end_time = start_time + best_processing_time
        
        schedule[job_id].append({
            'Operation': op_idx + 1,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })
        
        machine_available_time[best_machine] = end_time
        job_completion_time[job_id] = end_time
    
    return schedule
