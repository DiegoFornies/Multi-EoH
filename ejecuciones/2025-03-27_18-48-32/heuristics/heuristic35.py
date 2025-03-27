
def heuristic(input_data):
    """
    Heuristic scheduling for FJSSP: Prioritizes earliest finish time.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {}
    
    eligible_operations = []
    for job_id in range(1, n_jobs + 1):
        eligible_operations.append((job_id, 0))
    
    while eligible_operations:
        best_op = None
        min_end_time = float('inf')
        
        for job_id, op_idx in eligible_operations:
            machines, times = jobs_data[job_id][op_idx]
            
            for m_idx, machine in enumerate(machines):
                processing_time = times[m_idx]
                start_time = max(machine_available_time[machine], job_completion_time[job_id])
                end_time = start_time + processing_time
                
                if end_time < min_end_time:
                    min_end_time = end_time
                    best_op = (job_id, op_idx, machine, processing_time, start_time)
        
        if best_op is None:
            break
        
        job_id, op_idx, machine, processing_time, start_time = best_op
        
        if job_id not in schedule:
            schedule[job_id] = []
            
        op_num = op_idx + 1
        schedule[job_id].append({
            'Operation': op_num,
            'Assigned Machine': machine,
            'Start Time': start_time,
            'End Time': start_time + processing_time,
            'Processing Time': processing_time
        })
        
        machine_available_time[machine] = start_time + processing_time
        job_completion_time[job_id] = start_time + processing_time
        
        eligible_operations.remove((job_id, op_idx))
        
        next_op_idx = op_idx + 1
        if next_op_idx < len(jobs_data[job_id]):
            eligible_operations.append((job_id, next_op_idx))

    return schedule
