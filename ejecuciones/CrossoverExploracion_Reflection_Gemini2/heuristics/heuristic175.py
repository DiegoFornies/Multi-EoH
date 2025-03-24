
def heuristic(input_data):
    """
    FJSSP heuristic: SPT + Earliest Due Date (EDD) + Machine Load Balancing.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_time = {m: 0 for m in range(n_machines)}
    job_due_dates = {}
    schedule = {j: [] for j in jobs_data}

    # Calculate job due dates (sum of processing times)
    for job_id, job in jobs_data.items():
        total_time = 0
        for machines, times in job:
            total_time += min(times)
        job_due_dates[job_id] = total_time

    operations = []
    for job_id, job in jobs_data.items():
        for op_idx, (machines, times) in enumerate(job):
            operations.append({
                'job_id': job_id,
                'op_idx': op_idx + 1,
                'machines': machines,
                'times': times
            })

    job_current_operation = {j: 1 for j in jobs_data}
    available_operations = [op for op in operations if op['op_idx'] == job_current_operation[op['job_id']]]

    while available_operations:
        # Sort by SPT, EDD and machine load.
        available_operations.sort(key=lambda op: (min(op['times']), job_due_dates[op['job_id']], machine_available_time[min(op['machines'], key=lambda m: machine_available_time[m])]))

        operation = available_operations.pop(0)
        job_id = operation['job_id']
        op_idx = operation['op_idx']
        machines = operation['machines']
        times = operation['times']

        best_machine = None
        min_end_time = float('inf')
        processing_time = None

        for i in range(len(machines)):
            machine = machines[i]
            time = times[i]
            available_time = machine_available_time[machine]
            start_time = available_time
            end_time = start_time + time

            if end_time < min_end_time:
                min_end_time = end_time
                best_machine = machine
                processing_time = time

        start_time = machine_available_time[best_machine]
        end_time = start_time + processing_time

        schedule[job_id].append({
            'Operation': op_idx,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

        machine_available_time[best_machine] = end_time
        job_current_operation[job_id] += 1

        available_operations = [op for op in operations if op['job_id'] in jobs_data and op['op_idx'] == job_current_operation[op['job_id']]]

    return schedule
