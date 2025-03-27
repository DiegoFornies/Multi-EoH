
def heuristic(input_data):
    """Schedules jobs using SPT and earliest machine."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    job_remaining_times = {}

    # Calculate total processing time for each job.
    for job, operations in jobs_data.items():
        total_time = sum(min(times) for machines, times in operations)
        job_remaining_times[job] = total_time

    # Order jobs by remaining processing time (shortest first).
    job_order = sorted(job_remaining_times.keys(), key=job_remaining_times.get)

    for job in job_order:
        schedule[job] = []
        current_time = 0

        for op_idx, (machines, times) in enumerate(jobs_data[job]):
            op_num = op_idx + 1

            # Find the machine with the earliest available time among feasible machines.
            best_machine = None
            min_start_time = float('inf')
            best_processing_time = None

            for m_idx, machine in enumerate(machines):
                start_time = max(machine_available_time[machine], current_time)

                if start_time < min_start_time:
                    min_start_time = start_time
                    best_machine = machine
                    best_processing_time = times[m_idx]

            # Choose machine and assign operation.
            start_time = max(machine_available_time[best_machine], current_time)
            processing_time = best_processing_time
            end_time = start_time + processing_time

            schedule[job].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': processing_time
            })

            # Update machine available time and job completion time.
            machine_available_time[best_machine] = end_time
            current_time = end_time
            job_completion_time[job] = end_time

    return schedule
