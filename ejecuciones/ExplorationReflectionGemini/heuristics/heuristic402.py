
def heuristic(input_data):
    """Combines SPT, load balancing, and job urgency."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_load = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in jobs}
    schedule = {j: [] for j in jobs}
    job_total_processing_times = {j: sum(min(t) for _, t in ops) for j, ops in jobs.items()}
    available_jobs = sorted(jobs.keys(), key=lambda j: job_total_processing_times[j])
    job_operations_scheduled = {job: 0 for job in jobs}
    machine_available_times = {m: 0 for m in range(n_machines)}
    job_remaining_times = {}

    for job_id in range(1, n_jobs + 1):
        remaining_time = 0
        for machines, times in jobs[job_id]:
            remaining_time += min(times)
        job_remaining_times[job_id] = remaining_time

    while any(job_operations_scheduled[job] < len(jobs[job]) for job in jobs):
        for job in available_jobs:
            next_op_index = job_operations_scheduled[job]
            if next_op_index >= len(jobs[job]):
                continue

            machines, times = jobs[job][next_op_index]
            op_num = next_op_index + 1
            best_machine, best_start_time, processing_time = None, float('inf'), None
            min_cost = float('inf')
            for i, m in enumerate(machines):
                start_time = max(job_completion_times[job], machine_available_times[m])
                end_time = start_time + times[i]
                future_load = machine_load[m] + times[i]
                #cost = times[i] + 0.3 * future_load + 0.01 * start_time # Parent 2
                cost = end_time + 0.05 * machine_load[m] - 0.1 * job_remaining_times[job] # Parent 1
                if cost < min_cost:
                    min_cost = cost
                    best_machine = m
                    best_start_time = start_time
                    processing_time = times[i]

            if best_machine is not None:

                schedule[job].append({
                    'Operation': op_num,
                    'Assigned Machine': best_machine,
                    'Start Time': best_start_time,
                    'End Time': best_start_time + processing_time,
                    'Processing Time': processing_time
                })

                machine_load[best_machine] += processing_time
                machine_available_times[best_machine] = best_start_time + processing_time
                job_completion_times[job] = best_start_time + processing_time
                job_remaining_times[job] -= processing_time
                job_operations_scheduled[job] += 1

    return schedule
