
def heuristic(input_data):
    """
    Schedules jobs based on Shortest Processing Time (SPT) and earliest available machine,
    considering operation and machine feasibility.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in jobs}

    # Sort operations by shortest processing time among available machines
    operations = []
    for job, ops in jobs.items():
        for op_idx, (machines, times) in enumerate(ops):
            min_time = float('inf')
            best_machine = None

            for i, m in enumerate(machines):
                if times[i] < min_time:
                    min_time = times[i]
                    best_machine = m

            operations.append((min_time, job, op_idx, best_machine))

    operations.sort() # Sort by Shortest Processing Time first

    for _, job, op_idx, preferred_machine in operations:
        if job not in schedule:
            schedule[job] = []

        machines, times = jobs[job][op_idx]
        
        # Find best machine and corresponding processing time. Favor preferred if possible.
        best_machine = None
        best_time = float('inf')
        
        for i, m in enumerate(machines):
            if m == preferred_machine:
                best_machine = m
                best_time = times[i]
                break

        if best_machine is None: # Preferred machine not available. Find best of rest
            for i, m in enumerate(machines):
                if times[i] < best_time:
                    best_time = times[i]
                    best_machine = m

        # Ensure no overlap with previous operation within same job.
        start_time = max(machine_available_time[best_machine], job_completion_time[job])
        end_time = start_time + best_time

        schedule[job].append({
            'Operation': op_idx + 1,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_time
        })

        # Update machine and job completion times
        machine_available_time[best_machine] = end_time
        job_completion_time[job] = end_time

    return schedule
