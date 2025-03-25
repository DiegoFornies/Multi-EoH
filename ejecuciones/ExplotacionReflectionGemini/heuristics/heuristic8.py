
def heuristic(input_data):
    """
    A dispatching rule-based heuristic for FJSSP. 
    Chooses the shortest processing time operation among the available ones,
    prioritizing machine load balancing.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']
    
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_current_operation = {job: 0 for job in jobs_data}
    job_end_time = {job: 0 for job in jobs_data}
    schedule = {job: [] for job in jobs_data}
    
    completed_jobs = 0
    
    while completed_jobs < n_jobs:
        eligible_operations = []
        
        for job in jobs_data:
            if job_current_operation[job] < len(jobs_data[job]):
                eligible_operations.append(job)
                
        if not eligible_operations:
            break
            
        best_operation = None
        best_machine = None
        min_end_time = float('inf')
        
        for job in eligible_operations:
            op_idx = job_current_operation[job]
            machines, times = jobs_data[job][op_idx]
            
            for m_idx, machine in enumerate(machines):
                processing_time = times[m_idx]
                start_time = max(machine_available_time[machine], job_end_time[job])
                end_time = start_time + processing_time
                
                if end_time < min_end_time:
                    min_end_time = end_time
                    best_operation = (job, op_idx)
                    best_machine = machine
                    best_processing_time = processing_time
                    best_start_time = start_time
        
        job, op_idx = best_operation
        
        schedule[job].append({
            'Operation': op_idx + 1,
            'Assigned Machine': best_machine,
            'Start Time': best_start_time,
            'End Time': min_end_time,
            'Processing Time': best_processing_time
        })
        
        machine_available_time[best_machine] = min_end_time
        job_end_time[job] = min_end_time
        job_current_operation[job] += 1
        
        if job_current_operation[job] == len(jobs_data[job]):
            completed_jobs += 1
            
    return schedule
