
def heuristic(input_data):
    """
    Dynamically prioritizes operations based on job urgency and machine load.
    Uses a weighted combination to balance makespan and machine utilization.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {job: 0 for job in range(1, n_jobs + 1)}
    scheduled_operations = {job: [] for job in range(1, n_jobs + 1)}
    job_remaining_work = {job: sum(sum(op[1]) for op in jobs_data[job]) for job in range(1, n_jobs + 1)}
    
    eligible_operations = []
    for job, operations in jobs_data.items():
        eligible_operations.append((job, 1))
        
    while eligible_operations:
        best_op = None
        best_score = float('inf')
        best_machine = None
        best_time = None
        best_job = None
        
        for job, op_num in eligible_operations:
            machines, times = jobs_data[job][op_num - 1]
            
            for m_idx, m in enumerate(machines):
                start_time = max(machine_available_times[m], job_completion_times[job])
                processing_time = times[m_idx]
                
                # Dynamic Weighting (Urgency + Load)
                urgency = job_remaining_work[job]
                load = machine_available_times[m]
                score = start_time + 0.5*load - 0.3*urgency
                
                if score < best_score:
                    best_score = score
                    best_op = op_num
                    best_machine = m
                    best_time = processing_time
                    best_job = job
        
        start_time = max(machine_available_times[best_machine], job_completion_times[best_job])
        end_time = start_time + best_time
        scheduled_operations[best_job].append({
            'Operation': best_op,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_time
        })
        
        machine_available_times[best_machine] = end_time
        job_completion_times[best_job] = end_time
        job_remaining_work[best_job] -= best_time

        eligible_operations.remove((best_job, best_op))
        
        if best_op < len(jobs_data[best_job]):
            eligible_operations.append((best_job, best_op + 1))

    return scheduled_operations
