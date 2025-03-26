
def heuristic(input_data):
    """Combines SPT, earliest start, and dynamic load balancing for FJSSP."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_load = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in jobs}
    schedule = {j: [] for j in jobs}
    machine_available_times = {m: 0 for m in range(n_machines)}
    available_operations = []

    for job_id, operations in jobs.items():
        available_operations.append({'job': job_id, 'op_idx': 0})

    while available_operations:
        best_op = None
        min_cost = float('inf')

        for op_data in available_operations:
            job_id = op_data['job']
            op_idx = op_data['op_idx']
            machines, times = jobs[job_id][op_idx]

            for i, m in enumerate(machines):
                start_time = max(job_completion_times[job_id], machine_available_times[m])
                end_time = start_time + times[i]
                future_load = machine_load[m] + times[i]
                cost = times[i] + 0.2 * future_load + 0.1 * start_time # Prioritize processing time, load, and then start time

                if cost < min_cost:
                    min_cost = cost
                    best_op = op_data
                    best_machine = m
                    best_start_time = start_time
                    best_processing_time = times[i]

        job_id = best_op['job']
        op_idx = best_op['op_idx']
        op_num = op_idx + 1

        schedule[job_id].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': best_start_time,
            'End Time': best_start_time + best_processing_time,
            'Processing Time': best_processing_time
        })

        machine_load[best_machine] += best_processing_time
        machine_available_times[best_machine] = best_start_time + best_processing_time
        job_completion_times[job_id] = best_start_time + best_processing_time

        available_operations.remove(best_op)
        if op_idx + 1 < len(jobs[job_id]):
            available_operations.append({'job': job_id, 'op_idx': op_idx + 1})

    return schedule
