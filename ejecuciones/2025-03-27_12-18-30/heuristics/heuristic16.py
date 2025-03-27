
def heuristic(input_data):
    """
    Heuristic for FJSSP minimizing makespan and balancing machine load.
    Prioritizes operations with fewer machine options and shorter processing times.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {}
    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}

    # Create a list of operations with relevant information
    operations = []
    for job, ops in jobs_data.items():
        for op_idx, (machines, times) in enumerate(ops):
            operations.append({
                'job': job,
                'op_idx': op_idx,
                'machines': machines,
                'times': times,
                'op_num': op_idx + 1
            })

    # Sort operations by number of available machines and processing time (ascending)
    operations.sort(key=lambda x: (len(x['machines']), min(x['times'])))

    for operation in operations:
        job = operation['job']
        op_idx = operation['op_idx']
        machines = operation['machines']
        times = operation['times']
        op_num = operation['op_num']

        # Find the best machine based on earliest available time
        best_machine = None
        min_start_time = float('inf')
        processing_time = None

        for m_idx, machine in enumerate(machines):
            proc_time = times[m_idx]
            start_time = max(machine_available_times[machine], job_completion_times[job])

            if start_time < min_start_time:
                min_start_time = start_time
                best_machine = machine
                processing_time = proc_time

        # Schedule the operation on the selected machine
        start_time = min_start_time
        end_time = start_time + processing_time

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
        machine_available_times[best_machine] = end_time
        job_completion_times[job] = end_time

    return schedule
