
def heuristic(input_data):
    """Combines SPT and load balancing for FJSSP, adaptively."""

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {j: [] for j in range(1, n_jobs + 1)}

    available_operations = []
    for job_id in range(1, n_jobs + 1):
        available_operations.append({'job': job_id, 'op_idx': 0})

    while available_operations:
        best_op = None
        best_score = float('inf')

        for op_data in available_operations:
            job_id = op_data['job']
            op_idx = op_data['op_idx']
            machines, times = jobs[job_id][op_idx]

            for machine_idx, (machine, time) in enumerate(zip(machines, times)):
                start_time = max(machine_available_times[machine], job_completion_times[job_id])
                end_time = start_time + time

                # Score: weighted sum of SPT and load
                # Adaptively weight based on machine load. Higher load -> favor SPT less
                load_factor = machine_available_times[machine] / sum(machine_available_times.values()) if sum(machine_available_times.values()) > 0 else 0.0
                # Score:  load_factor*end_time + (1-load_factor)*time
                score = load_factor * end_time + (1 - load_factor) * time

                if score < best_score:
                    best_score = score
                    best_op = op_data
                    best_machine = machine
                    best_start_time = start_time
                    best_processing_time = time

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

        machine_available_times[best_machine] = best_start_time + best_processing_time
        job_completion_times[job_id] = best_start_time + best_processing_time

        available_operations.remove(best_op)
        if op_idx + 1 < len(jobs[job_id]):
            available_operations.append({'job': job_id, 'op_idx': op_idx + 1})

    return schedule
