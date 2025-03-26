
def heuristic(input_data):
    """Schedules jobs balancing SPT and machine load."""
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
        best_score = float('inf')

        for op_data in available_operations:
            job_id = op_data['job']
            op_idx = op_data['op_idx']
            machines, times = jobs[job_id][op_idx]

            min_cost = float('inf')
            selected_machine = None
            processing_time = None
            start_time_select = None

            for i, m in enumerate(machines):
                start_time = max(job_completion_times[job_id], machine_available_times[m])
                end_time = start_time + times[i]
                future_load = machine_load[m] + times[i]
                cost = times[i] + 0.3 * future_load + 0.01 * start_time

                if cost < min_cost:
                    min_cost = cost
                    selected_machine = m
                    processing_time = times[i]
                    start_time_select = start_time

            score = min_cost # load and SPT combined

            if score < best_score:
                best_score = score
                best_op = op_data

        job_id = best_op['job']
        op_idx = best_op['op_idx']
        op_num = op_idx + 1

        start_time = max(machine_available_times[selected_machine], job_completion_times[job_id])
        end_time = start_time + processing_time

        schedule[job_id].append({
            'Operation': op_num,
            'Assigned Machine': selected_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

        machine_load[selected_machine] += processing_time
        machine_available_times[selected_machine] = end_time
        job_completion_times[job_id] = end_time

        available_operations.remove(best_op)

        if op_idx + 1 < len(jobs[job_id]):
            available_operations.append({'job': job_id, 'op_idx': op_idx + 1})

    return schedule
