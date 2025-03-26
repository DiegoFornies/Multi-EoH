
def heuristic(input_data):
    """Hybrid heuristic: SPT-based scheduling with load balancing."""

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_load = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in jobs}
    schedule = {j: [] for j in jobs}

    available_operations = []
    for job_id, operations in jobs.items():
        available_operations.append({'job': job_id, 'op_idx': 0})

    while available_operations:
        best_op = None
        best_score = float('inf')

        for op_data in available_operations:
            job_id = op_data['job']
            op_idx = op_data['op_idx']
            machines, times = jobs[job_id][op_idx]

            best_machine = None
            best_time = float('inf')

            for machine_idx, (machine, time) in enumerate(machines):
                start_time = max(machine_load[machine], job_completion_times[job_id])
                score = start_time + time
                if score < best_score:
                    best_score = score
                    best_machine = machine
                    best_time = time

        job_id = available_operations[0]['job']
        op_idx = available_operations[0]['op_idx']
        machines, times = jobs[job_id][op_idx]
        op_num = op_idx + 1

        if best_machine is None:
             best_machine = machines[0]
             best_time = times[0]

        start_time = max(machine_load[best_machine], job_completion_times[job_id])
        end_time = start_time + best_time

        schedule[job_id].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_time
        })

        machine_load[best_machine] = end_time
        job_completion_times[job_id] = end_time

        available_operations.pop(0)
        if op_idx + 1 < len(jobs[job_id]):
            available_operations.append({'job': job_id, 'op_idx': op_idx + 1})

    return schedule
