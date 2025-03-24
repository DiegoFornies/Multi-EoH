
def heuristic(input_data):
    """
    FJSSP heuristic using SPT and machine availability, 
    balancing machine load and prioritizing sequence feasibility.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in jobs_data}
    schedule = {j: [] for j in jobs_data}
    job_current_operation = {j: 1 for j in jobs_data}

    operations = []
    for job_id, job in jobs_data.items():
        for op_idx, (machines, times) in enumerate(job):
            operations.append({
                'job_id': job_id,
                'op_idx': op_idx + 1,
                'machines': machines,
                'times': times
            })

    available_operations = [op for op in operations if op['op_idx'] == job_current_operation[op['job_id']]]

    while available_operations:
        # Sort by SPT, then machine load.
        available_operations.sort(key=lambda op: (min(op['times']), machine_available_time[op['machines'][op['times'].index(min(op['times']))]]))

        operation = available_operations.pop(0)

        job_id = operation['job_id']
        op_idx = operation['op_idx']
        machines = operation['machines']
        times = operation['times']

        best_machine = None
        min_end_time = float('inf')
        processing_time = None

        # Find best machine, considering load balancing
        for i in range(len(machines)):
            machine = machines[i]
            time = times[i]

            available_time = machine_available_time[machine]
            start_time = max(available_time, job_completion_time[job_id])
            end_time = start_time + time

            if end_time < min_end_time:
                min_end_time = end_time
                best_machine = machine
                processing_time = time

        start_time = max(machine_available_time[best_machine], job_completion_time[job_id])
        end_time = start_time + processing_time

        schedule[job_id].append({
            'Operation': op_idx,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

        machine_available_time[best_machine] = end_time
        job_completion_time[job_id] = end_time
        job_current_operation[job_id] += 1

        available_operations = [op for op in operations if op['op_idx'] == job_current_operation[op['job_id']]]

    return schedule
