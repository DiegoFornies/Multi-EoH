
def heuristic(input_data):
    """
    Heuristic for FJSSP: Prioritizes jobs with shorter total processing time
    and assigns operations to machines with the earliest available time,
    considering both machine and job completion times.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    # Calculate total processing time for each job
    job_processing_times = {}
    for job, ops in jobs_data.items():
        total_time = sum(min(times) for machines, times in ops)  # Shortest time for each operation
        job_processing_times[job] = total_time

    # Sort jobs by total processing time (shortest first)
    sorted_jobs = sorted(job_processing_times.items(), key=lambda item: item[1])

    schedule = {}
    machine_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {job: 0 for job in range(1, n_jobs + 1)}

    for job, _ in sorted_jobs:
        schedule[job] = []
        current_job_time = 0  # Initialize completion time for the job

        for op_idx, (machines, times) in enumerate(jobs_data[job]):
            op_num = op_idx + 1
            best_machine = None
            best_start_time = float('inf')
            best_processing_time = None

            # Find the best machine for the current operation
            for m_idx, m in enumerate(machines):
                start_time = max(machine_time[m], current_job_time)
                if start_time < best_start_time:
                    best_start_time = start_time
                    best_machine = m
                    best_processing_time = times[m_idx]

            # Schedule the operation on the best machine
            start = best_start_time
            end = start + best_processing_time
            schedule[job].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start,
                'End Time': end,
                'Processing Time': best_processing_time
            })

            # Update machine and job completion times
            machine_time[best_machine] = end
            current_job_time = end  # Update the current job completion time
            job_completion_time[job] = end


    return schedule
