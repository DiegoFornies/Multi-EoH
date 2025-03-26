
def heuristic(input_data):
    """FJSSP heuristic: Combines SPT, earliest start, and dynamic load balancing."""

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in jobs}
    machine_load = {m: 0 for m in range(n_machines)}
    schedule = {j: [] for j in jobs}

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

            for machine_idx, (machine, time) in enumerate(zip(machines, times)):
                start_time = max(machine_available_times[machine], job_completion_times[job_id])
                end_time = start_time + time
                # Dynamic weight based on machine load
                load_factor = 0.1 
                cost = time + load_factor * machine_load[machine] + start_time * 0.01

                if cost < min_cost:
                    min_cost = cost
                    best_op = op_data
                    best_machine = machine
                    best_time = time
                    best_start_time = start_time

        job_id = best_op['job']
        op_idx = best_op['op_idx']
        op_num = op_idx + 1

        schedule[job_id].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': best_start_time,
            'End Time': best_start_time + best_time,
            'Processing Time': best_time
        })

        machine_available_times[best_machine] = best_start_time + best_time
        job_completion_times[job_id] = best_start_time + best_time
        machine_load[best_machine] += best_time

        available_operations.remove(best_op)
        if op_idx + 1 < len(jobs[job_id]):
            available_operations.append({'job': job_id, 'op_idx': op_idx + 1})

    return schedule
