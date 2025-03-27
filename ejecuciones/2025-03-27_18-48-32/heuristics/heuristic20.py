
def heuristic(input_data):
    """
    Heuristic to schedule jobs, minimizing makespan, balancing load, and reducing idle time.
    Prioritizes operations with fewer machine options and shorter processing times to make better scheduling choices.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    # Initialize schedule and machine available times
    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {job: 0 for job in jobs_data}

    # Create a list of operations with job and operation indices for sorting
    operations = []
    for job, ops in jobs_data.items():
        for op_idx, (machines, times) in enumerate(ops):
            operations.append((job, op_idx, machines, times))

    # Sort operations based on the number of available machines (fewer first) and processing time (shorter first)
    operations.sort(key=lambda x: (len(x[2]), min(x[3])))

    # Schedule operations
    for job, op_idx, machines, times in operations:
        op_num = op_idx + 1
        best_machine, best_start_time, best_processing_time = None, float('inf'), None

        # Find the best machine for the operation
        for m_idx, machine in enumerate(machines):
            processing_time = times[m_idx]
            start_time = max(machine_available_time[machine], job_completion_time[job])

            if start_time < best_start_time:
                best_start_time = start_time
                best_machine = machine
                best_processing_time = processing_time

        # Update schedule
        if job not in schedule:
            schedule[job] = []

        end_time = best_start_time + best_processing_time
        schedule[job].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': best_start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })

        # Update machine and job completion times
        machine_available_time[best_machine] = end_time
        job_completion_time[job] = end_time

    return schedule
