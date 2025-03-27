
def heuristic(input_data):
    """Combines SPT and earliest machine availability for FJSSP."""
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
        if job not in schedule:
            schedule[job] = []

        current_time = 0
        for op_idx in range(len(jobs[job])):
            machines, times = jobs[job][op_idx]

            best_machine = None
            min_start_time = float('inf')
            best_processing_time = None

            for m_idx, m in enumerate(machines):
                processing_time = times[m_idx]
                start_time = max(machine_time[m], job_completion_time[job])
                end_time = start_time + processing_time

                if start_time < min_start_time:
                    min_start_time = start_time
                    best_machine = m
                    best_processing_time = processing_time

            start_time = min_start_time
            end_time = start_time + best_processing_time

            schedule[job].append({
                'Operation': op_idx + 1,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_processing_time
            })

            machine_time[best_machine] = end_time
            job_completion_time[job] = end_time
            current_time = end_time

    return schedule
