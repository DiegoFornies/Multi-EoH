
def heuristic(input_data):
    """
    Heuristic for FJSSP: Prioritizes shortest processing time (SPT) 
    and earliest machine available time to minimize makespan.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']
    
    schedule = {}
    machine_time = {m: 0 for m in range(n_machines)}  # Initialize machine available times
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)} # completion time for each job
    
    # Priority queue for operations, sorted by shortest processing time
    operation_queue = []
    for job, ops in jobs.items():
        operation_queue.append((job, 0))  # (job, operation_index)
    
    scheduled_operations = set() # keep track scheduled operations to avoid re-scheduling

    while operation_queue:
        # Find the job with the shortest next possible operation
        best_job, best_op_idx = None, None
        min_duration = float('inf')
        
        for job, op_idx in operation_queue:
            machines, times = jobs[job][op_idx]
            shortest_time = min(times)

            if shortest_time < min_duration:
                min_duration = shortest_time
                best_job, best_op_idx = job, op_idx
        
        job = best_job
        op_idx = best_op_idx
        operation_queue.remove((job, op_idx))

        machines, times = jobs[job][op_idx]
        op_num = op_idx + 1
        
        # Find the earliest available machine for this operation
        best_machine, best_start_time, best_processing_time = None, float('inf'), None
        
        for i, m in enumerate(machines):
            start_time = max(machine_time[m], job_completion_time[job])
            processing_time = times[i]
            
            if start_time < best_start_time:
                best_start_time = start_time
                best_machine = m
                best_processing_time = processing_time
        
        # Schedule the operation on the chosen machine
        start = best_start_time
        end = start + best_processing_time
        m = best_machine

        if job not in schedule:
            schedule[job] = []
        schedule[job].append({'Operation': op_num, 'Assigned Machine': m, 'Start Time': start, 'End Time': end, 'Processing Time': best_processing_time})
        
        machine_time[m] = end
        job_completion_time[job] = end
        
        # Add the next operation of the job to the queue, if it exists
        if op_idx + 1 < len(jobs[job]):
            operation_queue.append((job, op_idx + 1))
    
    return schedule
