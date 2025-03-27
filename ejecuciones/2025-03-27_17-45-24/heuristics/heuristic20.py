
def heuristic(input_data):
    """
    A scheduling heuristic for FJSSP minimizing makespan, idle time, and balancing machine load.
    Prioritizes operations with fewer machine options and shorter processing times.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    # Initialize data structures
    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {job: 0 for job in jobs_data}
    operations = []

    # Prepare operations list with job and op_idx information
    for job, ops in jobs_data.items():
        for op_idx, (machines, times) in enumerate(ops):
            operations.append((job, op_idx, machines, times))

    # Sort operations based on number of possible machines, then shortest processing time
    operations.sort(key=lambda x: (len(x[2]), min(x[3]))) # Prioritize operations with less machine choices and shorter time
    
    # Schedule operations
    for job, op_idx, machines, times in operations:
        op_num = op_idx + 1
        
        # Find best machine based on earliest available time
        best_machine = None
        min_start_time = float('inf')

        for m_idx, machine in enumerate(machines):
            start_time = max(machine_available_time[machine], job_completion_time[job])
            if start_time < min_start_time:
                min_start_time = start_time
                best_machine = machine
                best_time_index = m_idx

        processing_time = times[best_time_index]

        start_time = max(machine_available_time[best_machine], job_completion_time[job])
        end_time = start_time + processing_time

        # Update schedule
        if job not in schedule:
            schedule[job] = []

        schedule[job].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

        # Update machine and job completion times
        machine_available_time[best_machine] = end_time
        job_completion_time[job] = end_time

    return schedule
