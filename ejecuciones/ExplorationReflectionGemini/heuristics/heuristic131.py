
def heuristic(input_data):
    """Combines SPT job prioritization with machine load balancing."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in jobs}
    schedule = {j: [] for j in jobs}

    job_processing_times = {}
    for job, operations in jobs.items():
        total_time = sum(min(times) for _, times in operations)
        job_processing_times[job] = total_time

    available_jobs = sorted(jobs.keys(), key=lambda j: job_processing_times[j])
    job_operations_scheduled = {job: 0 for job in jobs}

    while any(job_operations_scheduled[job] < len(jobs[job]) for job in jobs):
        for job in available_jobs:
            next_op_index = job_operations_scheduled[job]
            if next_op_index >= len(jobs[job]):
                continue

            machines, times = jobs[job][next_op_index]
            op_num = next_op_index + 1

            best_machine = None
            min_start_time = float('inf')
            processing_time = None

            for i, m in enumerate(machines):
                start_time = max(machine_time[m], job_completion_time[job])
                if start_time < min_start_time:
                    min_start_time = start_time
                    best_machine = m
                    processing_time = times[i]

            if best_machine is not None:
                start_time = max(machine_time[best_machine], job_completion_time[job])
                end_time = start_time + processing_time

                schedule[job].append({
                    'Operation': op_num,
                    'Assigned Machine': best_machine,
                    'Start Time': start_time,
                    'End Time': end_time,
                    'Processing Time': processing_time
                })

                machine_time[best_machine] = end_time
                job_completion_time[job] = end_time
                job_operations_scheduled[job] += 1

    return schedule
