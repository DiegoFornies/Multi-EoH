
def heuristic(input_data):
    """
    A heuristic to schedule jobs considering machine availability and job dependencies.
    It prioritizes machines with earliest availability and minimizes idle time.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']
    
    schedule = {job: [] for job in jobs}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {job: 0 for job in jobs}
    
    # Sort operations by processing time to prioritize short operations
    operations = []
    for job, ops in jobs.items():
        for op_idx, (machines, times) in enumerate(ops):
            operations.append((job, op_idx, machines, times))

    def calculate_priority(job, op_idx):
        """Calculate priority based on job completion time and operation index."""
        return job_completion_time[job] + op_idx
    
    #operations.sort(key=lambda x: calculate_priority(x[0],x[1]))

    while operations:
        # Select the operation with the highest priority
        best_op = None
        best_priority = float('inf')
        for i in range(len(operations)):
          job, op_idx, machines, times = operations[i]
          priority = calculate_priority(job,op_idx)
          if priority < best_priority:
            best_priority = priority
            best_op = i

        job, op_idx, machines, times = operations.pop(best_op)
        
        # Find the earliest available machine
        best_machine, best_start_time, best_processing_time = None, float('inf'), None
        for m_idx in range(len(machines)):
          m = machines[m_idx]
          t = times[m_idx]
          start_time = max(machine_available_time[m], job_completion_time[job])
          
          if start_time < best_start_time:
            best_start_time = start_time
            best_machine = m
            best_processing_time = t
            
        # Schedule the operation
        start_time = best_start_time
        end_time = start_time + best_processing_time
        operation_number = op_idx+1
        
        schedule[job].append({
            'Operation': operation_number,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })
        
        # Update machine and job completion times
        machine_available_time[best_machine] = end_time
        job_completion_time[job] = end_time
        
    return schedule
