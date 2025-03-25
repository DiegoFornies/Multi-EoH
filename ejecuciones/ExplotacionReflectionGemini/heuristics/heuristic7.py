
def heuristic(input_data):
    """
    A heuristic algorithm for the Flexible Job Shop Scheduling Problem.
    Prioritizes operations with shorter processing times and balances machine load.
    """

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {}

    # Create a list of operations with job and operation indices
    operations = []
    for job, ops in jobs.items():
        for i, (machines, times) in enumerate(ops):
            operations.append((job, i + 1, machines, times))

    # Sort operations by shortest processing time
    operations.sort(key=lambda op: min(op[3]))

    for job, op_num, machines, times in operations:
        # Find the earliest available machine for this operation
        best_machine = None
        earliest_start_time = float('inf')
        best_processing_time = None

        for i, machine in enumerate(machines):
            processing_time = times[i]
            start_time = max(machine_available_times[machine], job_completion_times[job])

            if start_time < earliest_start_time:
                earliest_start_time = start_time
                best_machine = machine
                best_processing_time = processing_time

        # Assign the operation to the best machine
        start_time = earliest_start_time
        end_time = start_time + best_processing_time

        # Update machine and job completion times
        machine_available_times[best_machine] = end_time
        job_completion_times[job] = end_time

        # Add the operation to the schedule
        if job not in schedule:
            schedule[job] = []
        schedule[job].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })

    return schedule
