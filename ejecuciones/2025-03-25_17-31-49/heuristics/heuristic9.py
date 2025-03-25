
def heuristic(input_data):
    """
    Schedules jobs based on Shortest Processing Time (SPT) and earliest machine availability,
    aiming to minimize makespan and machine idle time.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {job: 0 for job in range(1, n_jobs + 1)}
    schedule = {}

    # Create a list of operations sorted by processing time
    operations = []
    for job_id, job_ops in jobs.items():
        for op_idx, (machines, times) in enumerate(job_ops):
            operations.append((job_id, op_idx + 1, machines, times))

    # Sort operations by shortest processing time (SPT)
    operations.sort(key=lambda x: min(x[3]))

    for job_id, op_num, machines, times in operations:
        best_machine = None
        min_end_time = float('inf')

        # Find the best machine for the current operation
        for i, machine in enumerate(machines):
            start_time = max(machine_available_time[machine], job_completion_time[job_id])
            end_time = start_time + times[i]

            if end_time < min_end_time:
                min_end_time = end_time
                best_machine = machine
                best_time = times[i]
                start_time_best = start_time

        # Schedule the operation on the best machine
        if job_id not in schedule:
            schedule[job_id] = []

        schedule[job_id].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start_time_best,
            'End Time': min_end_time,
            'Processing Time': best_time
        })

        # Update machine available time and job completion time
        machine_available_time[best_machine] = min_end_time
        job_completion_time[job_id] = min_end_time

    return schedule
