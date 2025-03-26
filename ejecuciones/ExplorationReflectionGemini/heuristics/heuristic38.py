
def heuristic(input_data):
    """Schedules jobs greedily, prioritizing shortest processing time on least loaded machine."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']
    
    machine_available_time = {m: 0 for m in range(n_machines)}
    machine_assignments = {m: [] for m in range(n_machines)} # Operations assigned to each machine
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)} # Completion time of each job
    schedule = {j: [] for j in range(1, n_jobs + 1)}
    
    # Initialize a list of operations, storing (job_id, operation_index)
    operations = []
    for job_id, job_ops in jobs.items():
        for op_idx in range(len(job_ops)):
            operations.append((job_id, op_idx))
    
    while operations:
        best_job_id, best_op_idx, best_machine, best_start_time, best_processing_time = None, None, None, float('inf'), None
        
        for job_id, op_idx in operations:
            machines, times = jobs[job_id][op_idx]
            
            for machine_idx, machine in enumerate(machines):
                processing_time = times[machine_idx]
                available_time = machine_available_time[machine]
                start_time = max(available_time, job_completion_time[job_id])
                
                if start_time < best_start_time:
                    best_job_id, best_op_idx = job_id, op_idx
                    best_machine = machine
                    best_start_time = start_time
                    best_processing_time = processing_time
        
        # Assign the best operation
        machine_assignments[best_machine].append((best_job_id, best_op_idx))
        start_time = best_start_time
        end_time = start_time + best_processing_time
        
        schedule[best_job_id].append({
            'Operation': best_op_idx + 1,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })
        
        machine_available_time[best_machine] = end_time
        job_completion_time[best_job_id] = end_time
        
        operations.remove((best_job_id, best_op_idx))
    
    return schedule
