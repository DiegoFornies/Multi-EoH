
def heuristic(input_data):
    """Combines SPT and load balancing for FJSSP."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_load = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in jobs}
    schedule = {j: [] for j in jobs}
    job_total_processing_times = {j: sum(min(t) for _, t in ops) for j, ops in jobs.items()}
    available_jobs = sorted(jobs.keys(), key=lambda j: job_total_processing_times[j])
    job_operations_scheduled = {job: 0 for job in jobs}

    machine_available_time = {m: 0 for m in range(n_machines)}

    while any(job_operations_scheduled[job] < len(jobs[job]) for job in jobs):
        for job in available_jobs:
            next_op_index = job_operations_scheduled[job]
            if next_op_index >= len(jobs[job]):
                continue

            machines, times = jobs[job][next_op_index]
            op_num = next_op_index + 1
            best_machine, min_completion_time, processing_time, start_time = None, float('inf'), None, None

            for i, m in enumerate(machines):
                processing_time_candidate = times[i]
                start_time_candidate = max(job_completion_times[job], machine_available_time[m])
                completion_time = start_time_candidate + processing_time_candidate

                load_balance_factor = machine_load[m]

                combined_metric = completion_time + 0.1 * load_balance_factor
                if combined_metric < min_completion_time:
                    min_completion_time = combined_metric
                    best_machine = m
                    processing_time = processing_time_candidate
                    start_time = start_time_candidate

            if best_machine is not None:
                end_time = start_time + processing_time

                schedule[job].append({
                    'Operation': op_num,
                    'Assigned Machine': best_machine,
                    'Start Time': start_time,
                    'End Time': end_time,
                    'Processing Time': processing_time
                })

                machine_load[best_machine] += processing_time
                machine_available_time[best_machine] = end_time
                job_completion_times[job] = end_time
                job_operations_scheduled[job] += 1

    return schedule
