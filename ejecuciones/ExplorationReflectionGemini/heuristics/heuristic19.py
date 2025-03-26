
def heuristic(input_data):
    """
    A heuristic for FJSSP prioritizing operations with the fewest machine options and shortest processing times.

    It aims to reduce makespan by scheduling critical operations early and balancing machine load.
    """

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    # Initialize machine availability times and job completion times
    machine_availability = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in jobs_data}

    # Create a list of operations with additional information
    operations = []
    for job, ops in jobs_data.items():
        for op_idx, (machines, times) in enumerate(ops):
            operations.append({
                'job': job,
                'op_idx': op_idx,
                'machines': machines,
                'times': times,
                'priority': len(machines),  # Fewer machines = higher priority
            })

    # Sort operations based on priority (fewest machines first)
    operations.sort(key=lambda x: x['priority'])

    schedule = {job: [] for job in jobs_data}

    # Process operations in the sorted order
    for op in operations:
        job = op['job']
        op_idx = op['op_idx']
        machines = op['machines']
        times = op['times']

        # Find the best machine and start time for this operation
        best_machine = None
        best_start_time = float('inf')
        best_processing_time = None

        for m_idx, machine in enumerate(machines):
            processing_time = times[m_idx]
            start_time = max(machine_availability[machine], job_completion_times[job])

            if start_time < best_start_time:
                best_start_time = start_time
                best_machine = machine
                best_processing_time = processing_time

        # Schedule the operation on the best machine at the best start time
        end_time = best_start_time + best_processing_time
        schedule[job].append({
            'Operation': op_idx + 1,
            'Assigned Machine': best_machine,
            'Start Time': best_start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })

        # Update machine availability and job completion time
        machine_availability[best_machine] = end_time
        job_completion_times[job] = end_time

    return schedule
