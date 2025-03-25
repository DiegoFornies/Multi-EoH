
def heuristic(input_data):
    """
    Heuristic scheduler for FJSSP that prioritizes minimizing idle time
    by selecting machines with the earliest available time.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in jobs}
    schedule = {j: [] for j in jobs}

    operations = []
    for job_id, job_ops in jobs.items():
        for op_idx, op in enumerate(job_ops):
            operations.append((job_id, op_idx, op))

    # Sort operations based on job ID and operation index to maintain job order
    operations.sort(key=lambda x: (x[0], x[1]))

    for job_id, op_idx, op in operations:
        machines, times = op
        best_machine, best_time, earliest_start = None, None, float('inf')

        # Find the machine that can start the operation the earliest
        for i, machine in enumerate(machines):
            available_time = machine_available_times[machine]
            start_time = max(available_time, job_completion_times[job_id])
            if start_time < earliest_start:
                earliest_start = start_time
                best_machine = machine
                best_time = times[i]

        start_time = earliest_start
        end_time = start_time + best_time

        schedule[job_id].append({
            'Operation': op_idx + 1,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_time
        })

        # Update machine and job completion times
        machine_available_times[best_machine] = end_time
        job_completion_times[job_id] = end_time

    return schedule
