
def heuristic(input_data):
    """Schedules jobs minimizing makespan using a shortest processing time approach."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    
    #Prioritize operations based on shortest processing time
    eligible_operations = []
    for job in range(1, n_jobs + 1):
        schedule[job] = []
        machines, times = jobs_data[job][0]
        min_time = min(times)
        eligible_operations.append((min_time, job, 0))  # (min_time, job, operation_index)
    
    eligible_operations.sort() #Sort all eligible operations by shortest processing time.
    
    while eligible_operations:
        min_time, job, op_idx = eligible_operations.pop(0)
        machines, times = jobs_data[job][op_idx]
        
        #Find the machine that makes the operation finish as early as possible.
        best_machine = None
        min_end_time = float('inf')
        best_processing_time = None

        for m_idx, machine in enumerate(machines):
            processing_time = times[m_idx]
            start_time = max(machine_available_time[machine], job_completion_time[job] if op_idx > 0 else 0)
            end_time = start_time + processing_time
            
            if end_time < min_end_time:
                min_end_time = end_time
                best_machine = machine
                best_processing_time = processing_time
                best_start_time = start_time
                
        start_time = best_start_time
        end_time = best_start_time + best_processing_time
        
        schedule[job].append({
                'Operation': op_idx + 1,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_processing_time
            })
            
        machine_available_time[best_machine] = end_time
        job_completion_time[job] = end_time
        
        if op_idx + 1 < len(jobs_data[job]):
            next_op_idx = op_idx + 1
            machines, times = jobs_data[job][next_op_idx]
            min_time = min(times)
            eligible_operations.append((min_time, job, next_op_idx))
            eligible_operations.sort()

    return schedule
