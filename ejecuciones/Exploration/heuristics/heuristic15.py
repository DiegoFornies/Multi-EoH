
def heuristic(input_data):
    """
    A heuristic to schedule jobs minimizing makespan by prioritizing operations
    with the shortest processing time and least available machines.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    # Initialize schedule and machine availability
    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in jobs}

    # Create a list of operations with job, operation index, available machines, and processing times
    operations = []
    for job_id, job_ops in jobs.items():
        for op_idx, (machines, times) in enumerate(job_ops):
            operations.append({
                'job_id': job_id,
                'op_idx': op_idx,
                'machines': machines,
                'times': times,
                'n_machines': len(machines)  # Track number of feasible machines
            })

    # Sort operations based on number of available machines (ascending) and processing time (ascending)
    operations.sort(key=lambda x: (x['n_machines'], min(x['times'])))  # Least slack machine first

    # Schedule each operation
    for op in operations:
        job_id = op['job_id']
        op_idx = op['op_idx']
        machines = op['machines']
        times = op['times']

        # Find the earliest available time on any feasible machine
        best_machine = None
        min_start_time = float('inf')
        best_processing_time = None

        for i, machine in enumerate(machines):
            processing_time = times[i]
            start_time = max(machine_available_time[machine], job_completion_time[job_id])

            if start_time < min_start_time:
                min_start_time = start_time
                best_machine = machine
                best_processing_time = processing_time

        # Assign operation to the chosen machine and update schedule
        start_time = min_start_time
        end_time = start_time + best_processing_time

        if job_id not in schedule:
            schedule[job_id] = []

        schedule[job_id].append({
            'Operation': op_idx + 1,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })

        # Update machine and job completion times
        machine_available_time[best_machine] = end_time
        job_completion_time[job_id] = end_time

    return schedule
