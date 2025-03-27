
def heuristic(input_data):
    """A heuristic for FJSSP that prioritizes minimizing idle time and balancing machine load."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {job: [] for job in jobs}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {job: 0 for job in jobs}

    # Create a list of operations with their associated data for easier sorting
    operations = []
    for job, ops in jobs.items():
        for op_idx, (machines, times) in enumerate(ops):
            operations.append({
                'job': job,
                'op_idx': op_idx,
                'machines': machines,
                'times': times,
                'op_num': op_idx + 1
            })

    # Sort operations based on shortest processing time (SPT)
    operations.sort(key=lambda x: min(x['times']))

    for operation in operations:
        job = operation['job']
        op_idx = operation['op_idx']
        machines = operation['machines']
        times = operation['times']
        op_num = operation['op_num']

        # Find the best machine for the operation, considering both machine availability and job completion time
        best_machine = None
        min_end_time = float('inf')

        for m_idx, machine in enumerate(machines):
            processing_time = times[m_idx]
            start_time = max(machine_available_time[machine], job_completion_time[job])
            end_time = start_time + processing_time

            if end_time < min_end_time:
                min_end_time = end_time
                best_machine = machine
                best_processing_time = processing_time
                best_start_time = start_time

        # Assign the operation to the best machine
        schedule[job].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': best_start_time,
            'End Time': best_start_time + best_processing_time,
            'Processing Time': best_processing_time
        })

        # Update machine availability and job completion time
        machine_available_time[best_machine] = best_start_time + best_processing_time
        job_completion_time[job] = best_start_time + best_processing_time

    return schedule
