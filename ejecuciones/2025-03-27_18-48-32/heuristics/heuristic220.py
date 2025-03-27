
def heuristic(input_data):
    """Schedules jobs by prioritizing operations based on a weighted score considering processing time, job urgency, and machine load."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {job: 0 for job in range(1, n_jobs + 1)}
    scheduled_operations = {job: [] for job in range(1, n_jobs + 1)}
    job_remaining_ops = {job: len(jobs_data[job]) for job in range(1, n_jobs + 1)} # Number of remaining operations
    
    eligible_operations = []
    for job, operations in jobs_data.items():
        eligible_operations.append((job, 1))
        
    while eligible_operations:
        best_op = None
        best_machine = None
        best_time = None
        best_job = None
        best_score = float('inf')
        
        for job, op_num in eligible_operations:
            machines, times = jobs_data[job][op_num - 1]
            
            for m_idx, m in enumerate(machines):
                start_time = max(machine_available_times[m], job_completion_times[job])
                processing_time = times[m_idx]
                
                # Calculate urgency score
                urgency = job_remaining_ops[job]
                
                # Calculate machine load penalty
                machine_load = machine_available_times[m]
                
                # Weighted score calculation
                score = (processing_time * 0.6) + (machine_load * 0.2) - (urgency * 0.2)
                
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
        job_remaining_ops[best_job] -= 1
        
        eligible_operations.remove((best_job, best_op))
        
        if best_op < len(jobs_data[best_job]):
            eligible_operations.append((best_job, best_op + 1))

    return scheduled_operations
