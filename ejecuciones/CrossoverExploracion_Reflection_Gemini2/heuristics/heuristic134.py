
def heuristic(input_data):
    """
    Schedule jobs using a greedy approach: earliest start time on machine.
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
                'times': times,
                'available_machines': machines
            })

    while True:
        available_operations = []
        for op in operations:
            if op['job_id'] in job_current_operation and op['op_idx'] == job_current_operation[op['job_id']]:
                available_operations.append(op)
        if not available_operations:
            break
        
        best_operation = None
        best_machine = None
        min_start_time = float('inf')
        processing_time = None

        for operation in available_operations:
            job_id = operation['job_id']
            machines = operation['available_machines']
            times = operation['times']

            for i in range(len(machines)):
                machine = machines[i]
                time = times[i]

                start_time = max(machine_available_time[machine], job_completion_time[job_id])

                if start_time < min_start_time:
                    min_start_time = start_time
                    best_machine = machine
                    best_operation = operation
                    processing_time = time
        
        if best_operation is None:
            break
        
        job_id = best_operation['job_id']
        op_idx = best_operation['op_idx']

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

    return schedule
