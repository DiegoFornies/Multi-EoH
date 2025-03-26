
def heuristic(input_data):
    """
    Schedules jobs using a Shortest Processing Time (SPT) and Earliest Start Time (EST) heuristic.
    Prioritizes operations with shorter processing times and schedules them on the earliest available machine.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in jobs_data}
    schedule = {j: [] for j in jobs_data}

    operations = []
    for job, ops in jobs_data.items():
        for op_idx, (machines, times) in enumerate(ops):
            operations.append((job, op_idx, machines, times))

    # Sort operations by shortest processing time (SPT)
    operations.sort(key=lambda x: min(x[3]))

    for job, op_idx, machines, times in operations:
        # Find the earliest available machine for the operation
        best_machine = None
        earliest_start_time = float('inf')
        processing_time = 0

        for i, machine in enumerate(machines):
            start_time = max(machine_available_time[machine], job_completion_time[job])
            if start_time < earliest_start_time:
                earliest_start_time = start_time
                best_machine = machine
                processing_time = times[i]  # Correctly obtain the processing time for the selected machine

        # Schedule the operation on the selected machine
        start_time = earliest_start_time
        end_time = start_time + processing_time

        schedule[job].append({
            'Operation': op_idx + 1,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

        # Update machine and job completion times
        machine_available_time[best_machine] = end_time
        job_completion_time[job] = end_time

    return schedule
