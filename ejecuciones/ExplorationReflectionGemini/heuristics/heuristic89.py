
def heuristic(input_data):
    """
    Hybrid FJSSP heuristic: Combines earliest completion time with machine load balancing.
    Prioritizes jobs with fewer machine choices and dynamically adjusts weights.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    machine_load = {m: 0 for m in range(n_machines)}
    job_completion_time = {job: 0 for job in jobs_data}

    available_operations = []
    next_operation = {}
    for job in jobs_data:
        next_operation[job] = 0
        if jobs_data[job]:
            machines, times = jobs_data[job][0]
            available_operations.append({
                'job': job,
                'op_idx': 0,
                'machines': machines,
                'times': times,
                'est': 0
            })

    while available_operations:
        available_operations.sort(key=lambda x: (len(x['machines']), x['est']))

        operation = available_operations.pop(0)

        job = operation['job']
        op_idx = operation['op_idx']
        machines = operation['machines']
        times = operation['times']

        best_machine = None
        min_weighted_time = float('inf')
        load_weight = 0.05  # Weight for machine load balancing
        time_weight = 1

        for i, machine in enumerate(machines):
            start_time = max(machine_available_time[machine], job_completion_time[job])
            completion_time = start_time + times[i]

            weighted_time = time_weight * completion_time + load_weight * machine_load[machine]

            if weighted_time < min_weighted_time:
                min_weighted_time = weighted_time
                best_machine = machine
                best_processing_time = times[i]
                best_start_time = start_time

        end_time = best_start_time + best_processing_time
        if job not in schedule:
            schedule[job] = []
        schedule[job].append({
            'Operation': op_idx + 1,
            'Assigned Machine': best_machine,
            'Start Time': best_start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })

        machine_available_time[best_machine] = end_time
        machine_load[best_machine] += best_processing_time
        job_completion_time[job] = end_time

        next_op_idx = next_operation[job] + 1
        next_operation[job] = next_op_idx

        if next_op_idx < len(jobs_data[job]):
            machines, times = jobs_data[job][next_op_idx]
            available_operations.append({
                'job': job,
                'op_idx': next_op_idx,
                'machines': machines,
                'times': times,
                'est': end_time
            })

    return schedule
