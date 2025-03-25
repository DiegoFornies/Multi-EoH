
def heuristic(input_data):
    """
    A heuristic for FJSSP that prioritizes shorter processing times and
    idle time reduction while respecting precedence constraints.
    """

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    # Initialize machine available times and job completion times
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in jobs_data}
    schedule = {j: [] for j in jobs_data}

    # Create a list of operations with job, operation number, and machine options
    operations = []
    for job_id, job_ops in jobs_data.items():
        for op_idx, (machines, times) in enumerate(job_ops):
            operations.append({
                'job': job_id,
                'operation': op_idx + 1,
                'machines': machines,
                'times': times,
                'precedence': job_completion_time[job_id]
            })

    # Sort operations based on shortest processing time on available machines
    operations.sort(key=lambda op: min(op['times']))  # Sort by shortest possible processing time

    # Schedule each operation
    for operation in operations:
        job_id = operation['job']
        op_num = operation['operation']
        machines = operation['machines']
        times = operation['times']
        precedence = operation['precedence']

        # Find the best machine to minimize completion time
        best_machine = None
        min_end_time = float('inf')

        for i, machine in enumerate(machines):
            start_time = max(machine_available_time[machine], precedence)
            end_time = start_time + times[i]

            if end_time < min_end_time:
                min_end_time = end_time
                best_machine = machine
                best_time = times[i]

        # Schedule the operation on the best machine
        start_time = max(machine_available_time[best_machine], precedence)
        end_time = start_time + best_time

        schedule[job_id].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_time
        })

        # Update machine available time and job completion time
        machine_available_time[best_machine] = end_time
        job_completion_time[job_id] = end_time

    return schedule
