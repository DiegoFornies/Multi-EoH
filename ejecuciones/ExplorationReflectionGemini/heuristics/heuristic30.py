
def heuristic(input_data):
    """
    A heuristic for FJSSP that prioritizes operations based on shortest processing time
    and minimizes machine idle time.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {job: [] for job in jobs}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {job: 0 for job in jobs}

    # Create a list of all operations, each with job, operation number, and available machines
    operations = []
    for job, ops in jobs.items():
        for i, (machines, times) in enumerate(ops):
            operations.append({
                'job': job,
                'operation': i + 1,
                'machines': machines,
                'times': times
            })

    # Sort operations by shortest processing time on the fastest available machine
    operations.sort(key=lambda op: min(op['times']))

    for operation in operations:
        job = operation['job']
        op_num = operation['operation']
        machines = operation['machines']
        times = operation['times']

        # Find the machine that can start the operation earliest
        best_machine = None
        earliest_start = float('inf')
        best_time = None

        for i, machine in enumerate(machines):
            start_time = max(machine_available_time[machine], job_completion_time[job])
            if start_time < earliest_start:
                earliest_start = start_time
                best_machine = machine
                best_time = times[i]

        # Schedule the operation on the best machine
        start_time = earliest_start
        end_time = start_time + best_time
        schedule[job].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_time
        })

        # Update machine available time and job completion time
        machine_available_time[best_machine] = end_time
        job_completion_time[job] = end_time

    return schedule
