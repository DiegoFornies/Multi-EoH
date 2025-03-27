
def heuristic(input_data):
    """Schedules jobs considering SPT, EDD, and machine availability."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_processing_times = {}

    for job, operations in jobs_data.items():
        total_time = sum(min(times) for machines, times in operations)
        job_processing_times[job] = total_time

    job_order = sorted(jobs_data.keys(), key=lambda job: (job_processing_times[job], job))

    for job in job_order:
        schedule[job] = []
        current_time = 0

        for op_idx, (machines, times) in enumerate(jobs_data[job]):
            op_num = op_idx + 1
            best_machine = None
            best_time = float('inf')
            best_processing_time = None

            for m_idx, machine in enumerate(machines):
                available_time = machine_available_time[machine]
                if available_time < best_time:
                    best_machine = machine
                    best_time = available_time
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

    return schedule
