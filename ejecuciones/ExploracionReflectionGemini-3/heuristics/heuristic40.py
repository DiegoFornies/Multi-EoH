
def heuristic(input_data):
    """
    A heuristic that prioritizes minimizing idle time between operations
    of the same job and balances machine load by selecting the machine
    with the earliest available time for each operation.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {job: [] for job in range(1, n_jobs + 1)}
    machine_available_time = {machine: 0 for machine in range(1, n_machines + 1)}
    job_completion_time = {job: 0 for job in range(1, n_jobs + 1)}

    # Create a list of operations to be scheduled
    operations = []
    for job, op_list in jobs.items():
        for op_idx, op in enumerate(op_list):
            operations.append((job, op_idx + 1, op))

    # Sort operations based on the earliest possible start time (SPT within job)
    operations.sort(key=lambda x: job_completion_time[x[0]])

    for job, op_num, op_data in operations:
        machines, times = op_data

        # Find the machine with the earliest available time among feasible machines
        best_machine = None
        min_end_time = float('inf')

        for i in range(len(machines)):
            machine = machines[i]
            processing_time = times[i]
            start_time = max(machine_available_time[machine], job_completion_time[job])
            end_time = start_time + processing_time

            if end_time < min_end_time:
                min_end_time = end_time
                best_machine = machine
                best_start_time = start_time
                best_processing_time = processing_time

        # Schedule the operation on the best machine
        schedule[job].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': best_start_time,
            'End Time': best_start_time + best_processing_time,
            'Processing Time': best_processing_time
        })

        # Update machine and job completion times
        machine_available_time[best_machine] = best_start_time + best_processing_time
        job_completion_time[job] = best_start_time + best_processing_time

    return schedule
