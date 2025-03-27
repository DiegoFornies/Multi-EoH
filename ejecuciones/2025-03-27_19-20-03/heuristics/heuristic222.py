
def heuristic(input_data):
    """Hybrid heuristic: Earliest Due Date and Least Loaded Machine."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    job_due_dates = {}
    job_ops = {j: 0 for j in range(1, n_jobs + 1)}
    machine_load = {m: 0 for m in range(n_machines)}

    # Estimate job due dates
    for job, operations in jobs_data.items():
        total_time = sum(min(times) for _, times in operations)
        job_due_dates[job] = total_time
        schedule[job] = []

    job_order = sorted(job_due_dates.keys(), key=job_due_dates.get)

    scheduled_operations = 0
    total_operations = sum(len(job_data) for job_data in jobs_data.values())
    
    while scheduled_operations < total_operations:
        eligible_operations = []
        for job_id in job_order:
            op_idx = job_ops[job_id]
            if op_idx < len(jobs_data[job_id]):
                eligible_operations.append((job_id, op_idx))
        
        best_operation = None
        best_machine = None
        min_end_time = float('inf')

        for job_id, op_idx in eligible_operations:
            machines, times = jobs_data[job_id][op_idx]
            for m_idx, machine in enumerate(machines):
                processing_time = times[m_idx]
                start_time = max(machine_available_time[machine], job_completion_time[job_id])
                end_time = start_time + processing_time
                
                #Tie breaker using machine load
                load_penalty = machine_load[machine]

                if end_time + load_penalty < min_end_time:
                    min_end_time = end_time + load_penalty
                    best_operation = (job_id, op_idx)
                    best_machine = machine
                    best_time = processing_time
                    best_start_time = start_time
                    
        if best_operation is None:
            break
            
        job_id, op_idx = best_operation
        
        schedule[job_id].append({
            'Operation': op_idx + 1,
            'Assigned Machine': best_machine,
            'Start Time': best_start_time,
            'End Time': best_start_time + best_time,
            'Processing Time': best_time
        })

        machine_available_time[best_machine] = best_start_time + best_time
        machine_load[best_machine] += best_time
        job_completion_time[job_id] = best_start_time + best_time
        job_ops[job_id] += 1
        scheduled_operations += 1
    
    return schedule
