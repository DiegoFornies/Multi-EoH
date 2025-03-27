
def heuristic(input_data):
    """
    A heuristic for FJSSP that prioritizes minimizing machine idle time
    and balances machine load by considering machine availability
    and operation processing times.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    # Initialize schedule and machine availability
    schedule = {job: [] for job in range(1, n_jobs + 1)}
    machine_availability = {m: 0 for m in range(n_machines)}

    # Initialize job completion times
    job_completion_times = {job: 0 for job in range(1, n_jobs + 1)}

    # Create a list of operations with their corresponding job number
    operations = []
    for job, ops in jobs_data.items():
        for op_idx, (machines, times) in enumerate(ops):
            operations.append((job, op_idx + 1, machines, times))

    # Sort operations based on the shortest processing time among feasible machines
    operations.sort(key=lambda x: min(x[3]))  # x[3] is times list

    # Schedule each operation
    for job, op_num, machines, times in operations:
        # Find the earliest available machine among the feasible machines
        best_machine = None
        min_start_time = float('inf')
        processing_time = None

        for i in range(len(machines)):
            machine = machines[i]
            time = times[i]

            start_time = max(machine_availability[machine], job_completion_times[job])

            if start_time < min_start_time:
                min_start_time = start_time
                best_machine = machine
                processing_time = time

        # Schedule the operation on the best machine
        start_time = min_start_time
        end_time = start_time + processing_time

        schedule[job].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

        # Update machine availability and job completion time
        machine_availability[best_machine] = end_time
        job_completion_times[job] = end_time  # consider it always, but job_completion_times[job] is only used in other job scheduling.

    return schedule
