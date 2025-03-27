
def heuristic(input_data):
    """Combines shortest processing time and earliest machine availability."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    job_ops = {job: 0 for job in jobs}
    job_remaining_times = {}

    # Calculate total processing time for each job.
    for job, operations in jobs.items():
        total_time = sum(min(times) for machines, times in operations)
        job_remaining_times[job] = total_time

    # Order jobs by remaining processing time (shortest first).
    job_order = sorted(job_remaining_times.keys(), key=job_remaining_times.get)

    for job in job_order:
        schedule[job] = []

        for op_idx in range(len(jobs[job])):
            machines, times = jobs[job][op_idx]

            # Find the machine with the earliest available time.
            best_machine = None
            min_start_time = float('inf')
            best_time = None

            for m_idx, machine in enumerate(machines):
                start_time = max(machine_time[machine], job_completion_time[job])

                if start_time < min_start_time:
                    min_start_time = start_time
                    best_machine = machine
                    best_time = times[m_idx]

            # Assign operation.
            start_time = min_start_time
            end_time = start_time + best_time

            schedule[job].append({
                'Operation': op_idx + 1,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_time
            })

            # Update machine available time and job completion time.
            machine_time[best_machine] = end_time
            job_completion_time[job] = end_time

    return schedule
