
def heuristic(input_data):
    """A heuristic for FJSSP that prioritizes earlier machine availability and shorter processing times."""

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {j: [] for j in range(1, n_jobs + 1)}

    # Create a list of operations to schedule
    operations = []
    for job_id, job_ops in jobs.items():
        for op_idx, (machines, times) in enumerate(job_ops):
            operations.append({
                'job_id': job_id,
                'op_idx': op_idx + 1,
                'machines': machines,
                'times': times
            })

    # Sort operations based on earliest possible start time to reduce idle time
    operations.sort(key=lambda op: min(max(machine_available_times[m], job_completion_times[op['job_id']]) for m in op['machines']))

    for operation in operations:
        job_id = operation['job_id']
        op_idx = operation['op_idx']
        machines = operation['machines']
        times = operation['times']

        # Find the machine with the earliest available time
        best_machine = None
        min_end_time = float('inf')

        for m_idx, machine in enumerate(machines):
            start_time = max(machine_available_times[machine], job_completion_times[job_id])
            end_time = start_time + times[m_idx]

            if end_time < min_end_time:
                min_end_time = end_time
                best_machine = machine
                processing_time = times[m_idx]
                start = start_time
                end = end_time

        # Update the schedule
        schedule[job_id].append({
            'Operation': op_idx,
            'Assigned Machine': best_machine,
            'Start Time': start,
            'End Time': end,
            'Processing Time': processing_time
        })

        # Update machine and job completion times
        machine_available_times[best_machine] = end
        job_completion_times[job_id] = end

    return schedule
