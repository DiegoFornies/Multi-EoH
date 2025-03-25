
def heuristic(input_data):
    """
    A heuristic for the Flexible Job Shop Scheduling Problem that prioritizes
    operations with shorter processing times and considers machine availability.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    # Initialize machine availability times and job completion times
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {job: 0 for job in range(1, n_jobs + 1)}
    schedule = {}

    # Create a list of operations sorted by processing time (shortest first)
    operations = []
    for job, ops in jobs_data.items():
        for op_idx, (machines, times) in enumerate(ops):
            operations.append((job, op_idx + 1, machines, times))

    operations.sort(key=lambda x: min(x[3]))  # Sort by shortest processing time

    # Schedule operations
    for job, op_num, machines, times in operations:
        # Find the earliest available machine and time for the operation
        best_machine = None
        earliest_start_time = float('inf')
        processing_time = None

        for i, machine in enumerate(machines):
            start_time = max(machine_available_time[machine], job_completion_time[job])
            if start_time < earliest_start_time:
                earliest_start_time = start_time
                best_machine = machine
                processing_time = times[i]

        # Schedule the operation on the best machine
        if job not in schedule:
            schedule[job] = []

        start_time = earliest_start_time
        end_time = start_time + processing_time

        schedule[job].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

        # Update machine and job completion times
        machine_available_time[best_machine] = end_time
        job_completion_time[job] = end_time

    return schedule
