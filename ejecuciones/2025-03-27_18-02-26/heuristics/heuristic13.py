
def heuristic(input_data):
    """
    Heuristic for FJSSP: Minimizes makespan by prioritizing operations
    with shortest processing time on least loaded machines.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']
    
    schedule = {}
    machine_load = {m: 0 for m in range(n_machines)}  # Keep track of machine load
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)} # Keep track of completion times
    
    # Create a list of all operations, along with their job and op indices
    operations = []
    for job, ops in jobs.items():
        for op_idx, (machines, times) in enumerate(ops):
            operations.append((job, op_idx, machines, times))

    # Sort operations based on shortest processing time
    operations.sort(key=lambda x: min(x[3]))

    for job, op_idx, machines, times in operations:
        op_num = op_idx + 1

        # Find the best machine for this operation (least loaded and available)
        best_machine, best_time = None, float('inf')
        for m_idx, m in enumerate(machines):
            available_time = machine_load[m]
            start_time = max(available_time, job_completion_times[job])
            processing_time = times[m_idx]
            
            if start_time < best_time:
                best_time = start_time
                best_machine = m
                chosen_processing_time = processing_time

        # Schedule the operation on the chosen machine
        start = best_time
        end = start + chosen_processing_time

        if job not in schedule:
            schedule[job] = []
        schedule[job].append({'Operation': op_num, 'Assigned Machine': best_machine, 'Start Time': start, 'End Time': end, 'Processing Time': chosen_processing_time})

        # Update machine load and job completion time
        machine_load[best_machine] = end
        job_completion_times[job] = end
    
    return schedule
