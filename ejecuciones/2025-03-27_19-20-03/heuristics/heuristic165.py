
def heuristic(input_data):
    """Hybrid: EDD-SPT for job order, SPT for machine."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    job_processing_times = {}

    for job, operations in jobs.items():
        total_time = sum(min(times) for machines, times in operations)
        job_processing_times[job] = total_time

    job_order = sorted(jobs.keys(), key=lambda job: (job, job_processing_times[job]))

    for job in job_order:
        schedule[job] = []
        current_time = job_completion_time[job] if job in job_completion_time else 0

        for op_idx, (machines, times) in enumerate(jobs[job]):
            op_num = op_idx + 1
            best_machine = None
            min_end_time = float('inf')
            processing_time = None

            for m_idx, machine in enumerate(machines):
                start_time = max(machine_time[machine], current_time)
                end_time = start_time + times[m_idx]
                if end_time < min_end_time:
                    min_end_time = end_time
                    best_machine = machine
                    processing_time = times[m_idx]

            start_time = max(machine_time[best_machine], current_time)
            end_time = start_time + processing_time

            schedule[job].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': processing_time
            })

            machine_time[best_machine] = end_time
            current_time = end_time
            job_completion_time[job] = current_time

    return schedule
