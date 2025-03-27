
def heuristic(input_data):
    """Schedules jobs based on a modified shortest remaining processing time (SRPT) heuristic."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    job_ops = {j: 0 for j in range(1, n_jobs + 1)}  # Track the current operation for each job

    # Calculate remaining processing time for each job
    job_remaining_time = {}
    for job in range(1, n_jobs + 1):
        remaining_time = 0
        for machines, times in jobs_data[job]:
            remaining_time += min(times)
        job_remaining_time[job] = remaining_time

    scheduled_jobs = set()
    while len(scheduled_jobs) < n_jobs:
        eligible_jobs = []
        for job in range(1, n_jobs + 1):
            if job not in scheduled_jobs:
                eligible_jobs.append(job)

        # Prioritize jobs with shortest remaining processing time
        if not eligible_jobs:
            break

        best_job = None
        min_remaining_time = float('inf')

        for job in eligible_jobs:
            if job_remaining_time[job] < min_remaining_time:
                min_remaining_time = job_remaining_time[job]
                best_job = job
        
        if best_job is None:
            break

        if best_job not in schedule:
            schedule[best_job] = []

        op_idx = job_ops[best_job]
        machines, times = jobs_data[best_job][op_idx]

        # Select the machine with earliest available time
        best_machine = None
        min_start_time = float('inf')
        best_processing_time = None

        for m_idx, machine in enumerate(machines):
            start_time = max(machine_available_time[machine], job_completion_time[best_job])
            if start_time < min_start_time:
                min_start_time = start_time
                best_machine = machine
                best_processing_time = times[m_idx]

        start_time = min_start_time
        processing_time = best_processing_time
        end_time = start_time + processing_time

        schedule[best_job].append({
            'Operation': op_idx + 1,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

        # Update machine available time and job completion time
        machine_available_time[best_machine] = end_time
        job_completion_time[best_job] = end_time
        job_ops[best_job] += 1
        job_remaining_time[best_job] -= processing_time #Update remaining time

        # If all operations for the job are completed
        if job_ops[best_job] == len(jobs_data[best_job]):
            scheduled_jobs.add(best_job)
    return schedule
