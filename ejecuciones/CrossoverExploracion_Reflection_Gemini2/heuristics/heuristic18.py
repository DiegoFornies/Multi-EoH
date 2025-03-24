
def heuristic(input_data):
    """
    A heuristic for FJSSP that prioritizes short operations
    and balances machine load using a shortest processing time (SPT) rule.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in jobs}

    # Create a list of all operations with job and operation indices
    all_operations = []
    for job, operations in jobs.items():
        for op_idx, (machines, times) in enumerate(operations):
            all_operations.append((job, op_idx, machines, times))

    # Sort operations by shortest processing time
    all_operations.sort(key=lambda x: min(x[3]))

    for job, op_idx, machines, times in all_operations:
        # Find the earliest available machine and time for the operation
        best_machine = None
        earliest_start_time = float('inf')
        processing_time = 0

        for m_idx, machine in enumerate(machines):
            start_time = max(machine_available_time[machine], job_completion_time[job])
            if start_time < earliest_start_time:
                earliest_start_time = start_time
                best_machine = machine
                processing_time = times[m_idx]

        # Schedule the operation on the best machine
        if job not in schedule:
            schedule[job] = []

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
