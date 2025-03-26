
def heuristic(input_data):
    """
    Heuristic for FJSSP: Schedules operations based on earliest completion time and machine availability,
    prioritizing operations with shorter processing times and balancing machine load.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']
    
    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in jobs_data}
    
    # Create a list of operations to schedule, sorted by job and operation number.
    operations = []
    for job, ops in jobs_data.items():
        for op_idx, (machines, times) in enumerate(ops):
            operations.append((job, op_idx + 1, machines, times))

    # Sort operations by estimated processing time to prioritize shorter operations.
    operations.sort(key=lambda op: min(op[3]))

    while operations:
        best_op = None
        best_machine = None
        earliest_start = float('inf')
        processing_time = None
        
        for job, op_num, machines, times in operations:
            for m_idx, machine in enumerate(machines):
                available_time = machine_available_time[machine]
                start_time = max(available_time, job_completion_time[job])
                
                if start_time < earliest_start:
                    earliest_start = start_time
                    best_op = (job, op_num, machines, times)
                    best_machine = machine
                    processing_time = times[m_idx] # Select correct time using the index.

        job, op_num, machines, times = best_op
        
        start_time = earliest_start
        end_time = start_time + processing_time
            
        if job not in schedule:
            schedule[job] = []
        
        schedule[job].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })
        
        machine_available_time[best_machine] = end_time
        job_completion_time[job] = end_time
        
        operations.remove(best_op)

    return schedule
