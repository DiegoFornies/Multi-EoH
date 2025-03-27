
def heuristic(input_data):
    """Prioritizes jobs with the fewest available machines."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    # Order jobs by the number of available machines for their first operation.
    job_priority = {job: len(jobs_data[job][0][0]) for job in jobs_data}
    job_order = sorted(job_priority.keys(), key=job_priority.get)

    for job in job_order:
        schedule[job] = []
        current_time = 0

        for op_idx, (machines, times) in enumerate(jobs_data[job]):
            op_num = op_idx + 1

            # Select machine with earliest available time.
            best_machine, best_time, best_processing_time = None, float('inf'), None
            for m_idx, machine in enumerate(machines):
                if machine_available_time[machine] < best_time:
                    best_machine = machine
                    best_time = machine_available_time[machine]
                    best_processing_time = times[m_idx]

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

            machine_available_time[best_machine] = end_time
            current_time = end_time
            job_completion_time[job] = end_time

    return schedule
