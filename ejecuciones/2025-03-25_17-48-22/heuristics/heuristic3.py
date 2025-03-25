
def heuristic(input_data):
    """
    Heuristic for FJSSP that prioritizes short processing times
    and balances machine load.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    # Create a list of operations with job and op index for sorting
    operations = []
    for job, ops in jobs.items():
        for op_idx, (machines, times) in enumerate(ops):
            operations.append((job, op_idx, machines, times))

    # Sort operations by shortest processing time first, then job number
    operations.sort(key=lambda x: min(x[3]))

    for job, op_idx, machines, times in operations:
        # Find the earliest available machine for the operation
        best_machine = None
        min_start_time = float('inf')
        processing_time = None
        
        for i, machine in enumerate(machines):
            available_time = max(machine_available_time[machine], job_completion_time[job])
            if available_time < min_start_time:
                min_start_time = available_time
                best_machine = machine
                processing_time = times[i]

        start_time = min_start_time
        end_time = start_time + processing_time
        machine_available_time[best_machine] = end_time
        job_completion_time[job] = end_time
        
        if job not in schedule:
            schedule[job] = []

        schedule[job].append({
            'Operation': op_idx + 1,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

    return schedule
