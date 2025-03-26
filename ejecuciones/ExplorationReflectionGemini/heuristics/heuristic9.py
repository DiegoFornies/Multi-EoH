
def heuristic(input_data):
    """
    A heuristic for the Flexible Job Shop Scheduling Problem (FJSSP) that prioritizes minimizing makespan.
    Chooses the machine for each operation that results in the earliest possible completion time.
    Considers both machine availability and job completion time.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_availability = {m: 0 for m in range(n_machines)}  # When each machine is next available
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)} # When each job is next available
    schedule = {j: [] for j in range(1, n_jobs + 1)} # Final Schedule

    operations = []  # List of tuples (job, operation index)

    # Initialize list of operations
    for job_id in range(1, n_jobs + 1):
        for op_idx in range(len(jobs[job_id])):
            operations.append((job_id, op_idx))

    # Sort operations based on shortest processing time (SPT) of the FIRST machine option
    operations.sort(key=lambda op: min(jobs[op[0]][op[1]][1]))

    # Process operations one by one
    for job_id, op_idx in operations:
        machines, times = jobs[job_id][op_idx]

        best_machine = None
        earliest_completion = float('inf')
        processing_time = None

        # Find the best machine for the current operation
        for i in range(len(machines)):
            machine = machines[i]
            time = times[i]
            start_time = max(machine_availability[machine], job_completion_times[job_id])
            completion_time = start_time + time

            if completion_time < earliest_completion:
                earliest_completion = completion_time
                best_machine = machine
                processing_time = time

        # Schedule the operation on the best machine
        start_time = max(machine_availability[best_machine], job_completion_times[job_id])
        end_time = start_time + processing_time

        schedule[job_id].append({
            'Operation': op_idx + 1,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

        # Update machine availability and job completion time
        machine_availability[best_machine] = end_time
        job_completion_times[job_id] = end_time
    return schedule
