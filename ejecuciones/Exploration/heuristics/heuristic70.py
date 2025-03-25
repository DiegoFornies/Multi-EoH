
def heuristic(input_data):
    """Hybrid heuristic: Job priority & machine availability."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in jobs}

    remaining_ops = {job: list(range(len(ops))) for job, ops in jobs.items()}
    job_priority = sorted(jobs.keys(), key=lambda job: len(remaining_ops[job]), reverse=True)

    while any(remaining_ops[job] for job in jobs):
        for job_id in job_priority:
            if not remaining_ops[job_id]:
                continue

            op_idx = remaining_ops[job_id][0]
            machines, times = jobs[job_id][op_idx]

            best_machine = None
            min_end_time = float('inf')
            best_start_time = None
            best_processing_time = None

            for m_idx, machine in enumerate(machines):
                start_time = max(machine_available_time[machine], job_completion_time[job_id])
                processing_time = times[m_idx]
                end_time = start_time + processing_time

                if end_time < min_end_time:
                    min_end_time = end_time
                    best_machine = machine
                    best_start_time = start_time
                    best_processing_time = processing_time

            if job_id not in schedule:
                schedule[job_id] = []

            schedule[job_id].append({
                'Operation': op_idx + 1,
                'Assigned Machine': best_machine,
                'Start Time': best_start_time,
                'End Time': min_end_time,
                'Processing Time': best_processing_time
            })

            machine_available_time[best_machine] = min_end_time
            job_completion_time[job_id] = min_end_time
            remaining_ops[job_id].pop(0)

    return schedule
