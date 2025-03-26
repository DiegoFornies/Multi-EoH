
def heuristic(input_data):
    """Combines SPT for job order with machine load balancing."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_load = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {j: [] for j in range(1, n_jobs + 1)}
    job_total_processing_times = {j: sum(min(t) for _, t in ops) for j, ops in jobs.items()}
    available_jobs = sorted(range(1, n_jobs + 1), key=lambda j: job_total_processing_times[j] if j in jobs else float('inf')) # sort jobs based on SPT
    job_operations_scheduled = {job: 0 for job in range(1, n_jobs + 1)}

    while any(job_operations_scheduled[job] < len(jobs[job]) for job in range(1, n_jobs + 1) if job in jobs):
        for job in available_jobs:
            if job not in jobs or job_operations_scheduled[job] >= len(jobs[job]):
                continue

            next_op_index = job_operations_scheduled[job]
            machines, times = jobs[job][next_op_index]
            op_num = next_op_index + 1
            best_machine, min_weighted_time, processing_time = None, float('inf'), None

            for i, m in enumerate(machines):
                start_time = max(job_completion_times[job], machine_load[m])
                weighted_time = start_time + times[i] + 0.05 * machine_load[m]
                if weighted_time < min_weighted_time:
                    min_weighted_time = weighted_time
                    best_machine = m
                    processing_time = times[i]

            if best_machine is not None:
                start_time = max(job_completion_times[job], machine_load[best_machine])
                end_time = start_time + processing_time

                schedule[job].append({
                    'Operation': op_num,
                    'Assigned Machine': best_machine,
                    'Start Time': start_time,
                    'End Time': end_time,
                    'Processing Time': processing_time
                })

                machine_load[best_machine] = end_time
                job_completion_times[job] = end_time
                job_operations_scheduled[job] += 1

    return schedule
