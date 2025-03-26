
def heuristic(input_data):
    """
    A heuristic for FJSSP that prioritizes shortest processing time
    and earliest available machine to minimize makespan.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in jobs}

    # Sort operations by shortest processing time across possible machines
    operations = []
    for job, ops in jobs.items():
        for op_idx, (machines, times) in enumerate(ops):
            min_time = min(times)
            operations.append((min_time, job, op_idx, machines, times))

    operations.sort()  # Sort by shortest processing time first

    for _, job, op_idx, machines, times in operations:
        op_num = op_idx + 1

        # Find the machine with the earliest available time among feasible machines
        best_machine = None
        earliest_start_time = float('inf')
        best_processing_time = None

        for m_idx, m in enumerate(machines):
            start_time = max(machine_available_times[m], job_completion_times[job])
            if start_time < earliest_start_time:
                earliest_start_time = start_time
                best_machine = m
                best_processing_time = times[m_idx]

        # Schedule the operation on the selected machine
        start_time = earliest_start_time
        end_time = start_time + best_processing_time

        if job not in schedule:
            schedule[job] = []

        schedule[job].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })

        # Update machine availability and job completion time
        machine_available_times[best_machine] = end_time
        job_completion_times[job] = end_time

    return schedule
