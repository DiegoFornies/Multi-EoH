
def heuristic(input_data):
    """
    A heuristic for the FJSSP that considers machine load balancing
    and operation dependencies to minimize makespan.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    # Initialize schedule and machine available times
    schedule = {job: [] for job in jobs}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {job: 0 for job in jobs}

    # Create a list of operations with job and operation indices
    operations = []
    for job, ops in jobs.items():
        for op_idx, (machines, times) in enumerate(ops):
            operations.append((job, op_idx, machines, times))

    # Sort operations based on shortest processing time on the first possible machine
    operations.sort(key=lambda x: x[3][0])  # x[3] refers to times which is the last element of the tuple

    # Schedule operations
    for job, op_idx, machines, times in operations:
        op_num = op_idx + 1

        # Find the machine with the earliest available time among possible machines
        best_machine = None
        min_start_time = float('inf')

        for i in range(len(machines)):
            m = machines[i]
            t = times[i]
            start_time = max(machine_available_time[m], job_completion_time[job])

            if start_time < min_start_time:
                min_start_time = start_time
                best_machine = m
                processing_time = t

        # Assign the operation to the best machine
        start_time = max(machine_available_time[best_machine], job_completion_time[job])
        end_time = start_time + processing_time

        schedule[job].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

        # Update machine available time and job completion time
        machine_available_time[best_machine] = end_time
        job_completion_time[job] = end_time

    return schedule
