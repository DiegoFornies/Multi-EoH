
def heuristic(input_data):
    """
    Heuristic for FJSSP minimizing makespan using shortest processing time first.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    # Create a list of all operations with job and operation number
    operations = []
    for job, ops in jobs.items():
        for op_idx, (machines, times) in enumerate(ops):
            operations.append((job, op_idx + 1, machines, times))

    # Sort operations by shortest processing time.  Break ties arbitrarily.
    operations.sort(key=lambda x: min(x[3]))  # Sort by min processing time

    for job, op_num, machines, times in operations:
        # Find the earliest available machine and time for the operation
        best_machine = None
        earliest_start_time = float('inf')
        processing_time = None

        for i in range(len(machines)):
            machine = machines[i]
            time = times[i]
            start_time = max(machine_available_time[machine], job_completion_time[job])

            if start_time < earliest_start_time:
                earliest_start_time = start_time
                best_machine = machine
                processing_time = time

        # Schedule the operation on the chosen machine
        start_time = earliest_start_time
        end_time = start_time + processing_time

        # Update machine and job completion times
        machine_available_time[best_machine] = end_time
        job_completion_time[job] = end_time

        # Add operation to the schedule
        if job not in schedule:
            schedule[job] = []
        schedule[job].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

    return schedule
