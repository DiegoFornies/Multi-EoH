
def heuristic(input_data):
    """Schedules jobs using a modified shortest processing time (SPT) with machine consideration."""

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_load = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in jobs}
    schedule = {j: [] for j in jobs}

    # Create a list of all operations with job, operation index, machines, and times
    operations = []
    for job, ops in jobs.items():
        for op_idx, (machines, times) in enumerate(ops):
            operations.append((job, op_idx, machines, times))

    # Sort operations based on the shortest processing time available across all machines
    operations.sort(key=lambda x: min(x[3]))

    for job, op_idx, machines, times in operations:
        op_num = op_idx + 1
        best_machine = None
        min_start_time = float('inf')
        processing_time = None

        #Find best machine based on the earliest finish time
        for i, m in enumerate(machines):
            start_time = max(job_completion_times[job], machine_load[m])
            if start_time < min_start_time:
                min_start_time = start_time
                best_machine = m
                processing_time = times[i]

        # Schedule the operation
        start_time = max(job_completion_times[job], machine_load[best_machine])
        end_time = start_time + processing_time

        schedule[job].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

        machine_load[best_machine] = end_time
        job_completion_times[job] = end_time

    return schedule
