
def heuristic(input_data):
    """Combines SPT job prioritization and machine load balancing."""

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in jobs}
    schedule = {j: [] for j in jobs}

    # Prioritize jobs by shortest processing time (SPT)
    job_processing_times = {}
    for job, operations in jobs.items():
        total_time = sum(min(times) for machines, times in operations)
        job_processing_times[job] = total_time
    job_priority = sorted(jobs.keys(), key=lambda job: job_processing_times[job])

    for job in job_priority:
        for op_idx, (machines, times) in enumerate(jobs[job]):
            op_num = op_idx + 1

            # Find the machine with the earliest available time
            best_machine = None
            earliest_start_time = float('inf')
            processing_time = None

            for i, machine in enumerate(machines):
                start_time = max(machine_time[machine], job_completion_time[job])
                if start_time < earliest_start_time:
                    earliest_start_time = start_time
                    best_machine = machine
                    processing_time = times[i]

            # Schedule operation on the best machine
            start_time = max(machine_time[best_machine], job_completion_time[job])
            end_time = start_time + processing_time

            schedule[job].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': processing_time
            })

            machine_time[best_machine] = end_time
            job_completion_time[job] = end_time

    return schedule
