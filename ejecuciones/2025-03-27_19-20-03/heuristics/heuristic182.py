
def heuristic(input_data):
    """Combines EDD and SPT with earliest machine."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    job_processing_times = {}

    for job, operations in jobs_data.items():
        total_time = sum(min(times) for machines, times in operations)
        job_processing_times[job] = total_time

    job_order = sorted(jobs_data.keys(), key=lambda job: (job, job_processing_times[job]))

    for job in job_order:
        schedule[job] = []
        current_time = 0
        for op_idx, (machines, times) in enumerate(jobs_data[job]):
            op_num = op_idx + 1
            best_machine = None
            min_end_time = float('inf')
            best_start_time = 0
            best_processing_time = 0

            for m_idx, machine in enumerate(machines):
                processing_time = times[m_idx]
                start_time = max(machine_available_time[machine], current_time)
                end_time = start_time + processing_time

                if end_time < min_end_time:
                    min_end_time = end_time
                    best_machine = machine
                    best_start_time = start_time
                    best_processing_time = processing_time

            schedule[job].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': best_start_time,
                'End Time': best_start_time + best_processing_time,
                'Processing Time': best_processing_time
            })

            machine_available_time[best_machine] = best_start_time + best_processing_time
            current_time = best_start_time + best_processing_time
            job_completion_time[job] = current_time

    return schedule
