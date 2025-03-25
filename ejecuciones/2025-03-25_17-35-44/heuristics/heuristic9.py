
def heuristic(input_data):
    """A heuristic for FJSSP that minimizes makespan, idle time, and machine load."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    # Initialize schedule, machine availability, and job completion times
    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in jobs}

    # Sort operations by shortest processing time first (SPT)
    operations = []
    for job, ops in jobs.items():
        for op_idx, (machines, times) in enumerate(ops):
            for m_idx, m in enumerate(machines):
                operations.append((times[m_idx], job, op_idx, m))

    operations.sort()  # Sort by processing time
    
    for time, job, op_idx, machine in operations:
        # Assign the earliest available time slot on chosen machine, considering precedence
        start_time = max(machine_available_time[machine], job_completion_time[job])
        end_time = start_time + time

        if job not in schedule:
            schedule[job] = []

        schedule[job].append({
            'Operation': op_idx + 1,
            'Assigned Machine': machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': time
        })

        # Update machine and job completion times
        machine_available_time[machine] = end_time
        job_completion_time[job] = end_time

    return schedule
