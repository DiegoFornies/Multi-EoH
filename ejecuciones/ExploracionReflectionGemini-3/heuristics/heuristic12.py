
def heuristic(input_data):
    """
    A heuristic for the Flexible Job Shop Scheduling Problem (FJSSP).
    It prioritizes jobs with the fewest possible machine options for each operation,
    selecting the machine with the earliest available time.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {job: 0 for job in range(1, n_jobs + 1)}

    # Create a list of jobs to schedule, prioritizing those with more constrained operations
    job_queue = list(jobs.keys())

    while job_queue:
        # Prioritize jobs based on the minimum number of machine choices available for their remaining operations
        job = min(job_queue, key=lambda j: min(len(op[0]) for op in jobs[j]))
        job_queue.remove(job)

        schedule[job] = []
        job_time = job_completion_time[job]

        for op_idx, (machines, times) in enumerate(jobs[job]):
            op_num = op_idx + 1

            # Choose the machine that becomes available the soonest
            best_machine = -1
            best_time = float('inf')
            best_processing_time = -1

            for m_idx, machine in enumerate(machines):
                available_time = machine_available_time[machine]
                start_time = max(available_time, job_time)
                if start_time < best_time:
                    best_time = start_time
                    best_machine = machine
                    best_processing_time = times[m_idx]

            start_time = best_time
            end_time = start_time + best_processing_time

            schedule[job].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': best_processing_time
            })

            machine_available_time[best_machine] = end_time
            job_time = end_time
        job_completion_time[job] = job_time

    return schedule
