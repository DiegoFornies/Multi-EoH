
def heuristic(input_data):
    """Schedules jobs by Earliest Due Date (EDD) and Shortest Processing Time (SPT) on machines."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    # Calculate the total processing time for each job to use as a tie-breaker.
    job_processing_times = {}
    for job, operations in jobs_data.items():
        total_time = sum(min(times) for machines, times in operations)
        job_processing_times[job] = total_time
    
    # Use job number as the due date proxy.  Sort jobs based on this proxy, then SPT.
    job_order = sorted(jobs_data.keys(), key=lambda job: (job, job_processing_times[job]))

    for job in job_order:
        schedule[job] = []
        current_time = 0

        for op_idx, (machines, times) in enumerate(jobs_data[job]):
            op_num = op_idx + 1

            # Find the machine that becomes available earliest.
            best_machine = None
            best_time = float('inf')
            best_processing_time = None

            for m_idx, machine in enumerate(machines):
                if machine_available_time[machine] < best_time:
                    best_machine = machine
                    best_time = machine_available_time[machine]
                    best_processing_time = times[m_idx]

            # Schedule the operation on the selected machine.
            start_time = max(best_time, current_time)
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
