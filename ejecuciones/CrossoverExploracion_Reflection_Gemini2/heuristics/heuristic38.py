
def heuristic(input_data):
    """
    Schedules operations using a shortest processing time and earliest start time strategy.
    Prioritizes operations with shorter processing times and assigns them to machines
    where they can start earliest, minimizing makespan and idle time.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {job: 0 for job in jobs_data}
    schedule = {job: [] for job in jobs_data}

    # Create a list of all operations and their possible schedules
    operations = []
    for job, operations_list in jobs_data.items():
        for op_idx, (machines, times) in enumerate(operations_list):
            operations.append({
                'job': job,
                'op_idx': op_idx,
                'machines': machines,
                'times': times
            })

    # Sort operations based on shortest processing time
    operations.sort(key=lambda op: min(op['times']))

    for operation in operations:
        job = operation['job']
        op_idx = operation['op_idx']
        machines = operation['machines']
        times = operation['times']

        best_machine = None
        best_start_time = float('inf')
        best_processing_time = None

        # Find the best machine and start time for the current operation
        for i, machine in enumerate(machines):
            processing_time = times[i]
            start_time = max(machine_available_times[machine], job_completion_times[job])

            if start_time < best_start_time:
                best_start_time = start_time
                best_machine = machine
                best_processing_time = processing_time

        # Schedule the operation on the chosen machine
        end_time = best_start_time + best_processing_time
        schedule[job].append({
            'Operation': op_idx + 1,
            'Assigned Machine': best_machine,
            'Start Time': best_start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })

        # Update machine and job completion times
        machine_available_times[best_machine] = end_time
        job_completion_times[job] = end_time

    return schedule
