
def heuristic(input_data):
    """Schedules jobs considering machine load & job processing time."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_load = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in jobs}
    schedule = {j: [] for j in jobs}
    job_total_processing_times = {}
    for job, operations in jobs.items():
        total_time = 0
        for machines, times in operations:
            total_time += min(times)
        job_total_processing_times[job] = total_time
    available_jobs = sorted(list(jobs.keys()), key=lambda x: job_total_processing_times[x])
    job_operations_scheduled = {job: 0 for job in jobs}

    while any(job_operations_scheduled[job] < len(jobs[job]) for job in jobs):
        for job in list(jobs.keys()):
            next_op_index = job_operations_scheduled[job]
            if next_op_index >= len(jobs[job]):
                continue
            machines, times = jobs[job][next_op_index]
            op_num = next_op_index + 1
            best_machine = None
            min_completion_time = float('inf')
            processing_time = None

            for i, m in enumerate(machines):
                processing_time = times[i]
                start_time = max(job_completion_times[job], machine_load[m])
                completion_time = start_time + processing_time
                combined_metric = completion_time + 0.1 * machine_load[m]

                if combined_metric < min_completion_time:
                    min_completion_time = combined_metric
                    best_machine = m
                    best_start_time = start_time
                    best_processing_time = processing_time

            if best_machine is not None:
                start_time = best_start_time
                end_time = best_start_time + best_processing_time

                schedule[job].append({
                    'Operation': op_num,
                    'Assigned Machine': best_machine,
                    'Start Time': start_time,
                    'End Time': end_time,
                    'Processing Time': best_processing_time
                })
                machine_load[best_machine] = end_time
                job_completion_times[job] = end_time
                job_operations_scheduled[job] += 1
    return schedule
