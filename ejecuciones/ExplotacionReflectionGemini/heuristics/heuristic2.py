
def heuristic(input_data):
    """
    Heuristic for FJSSP: Prioritizes operations with shortest processing time,
    assigning them to the earliest available machine to minimize makespan.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines + 1)}  # Initialize available times for each machine
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}  # Initialize completion times for each job
    schedule = {}

    # Flatten operations, associating them with their job
    operations = []
    for job_id, job_ops in jobs_data.items():
        for op_idx, (machines, times) in enumerate(job_ops):
            operations.append((job_id, op_idx + 1, machines, times))

    # Sort operations by shortest processing time.
    operations.sort(key=lambda x: min(x[3]))

    for job_id, op_num, machines, times in operations:
        # Find the machine and processing time that allows the earliest start
        best_machine = None
        best_time = None
        earliest_start = float('inf')

        for i in range(len(machines)):
            machine = machines[i]
            time = times[i]
            start_time = max(machine_available_times[machine], job_completion_times[job_id])

            if start_time < earliest_start:
                earliest_start = start_time
                best_machine = machine
                best_time = time

        # Schedule the operation on the chosen machine
        start_time = earliest_start
        end_time = start_time + best_time

        # Update machine available time and job completion time
        machine_available_times[best_machine] = end_time
        job_completion_times[job_id] = end_time

        # Add operation to the schedule
        if job_id not in schedule:
            schedule[job_id] = []

        schedule[job_id].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_time
        })

    return schedule
