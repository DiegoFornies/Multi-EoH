
def heuristic(input_data):
    """Combines EFT and machine load to minimize makespan."""
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
        best_operation = None
        min_end_time = float('inf')
        best_machine = None
        processing_time = None
        start = None

        for operation in available_operations:
            job_id = operation['job_id']
            machines = operation['machines']
            times = operation['times']

            for i in range(len(machines)):
                machine = machines[i]
                time = times[i]

                available_time = machine_available_time[machine]
                start_time = max(available_time, job_completion_time[job_id])
                end_time = start_time + time

                # Prioritize less loaded machines, break ties with EFT
                load_priority = machine_available_time[machine]
                if end_time - 0.01 * load_priority < min_end_time: # adjust the weight as needed
                    min_end_time = end_time - 0.01 * load_priority
                    best_operation = operation
                    best_machine = machine
                    processing_time = time
                    start = start_time

        if best_operation is not None:
            job_id = best_operation['job_id']
            op_idx = best_operation['op_idx']

            schedule[job_id].append({
                'Operation': op_idx,
                'Assigned Machine': best_machine,
                'Start Time': start,
                'End Time': start + processing_time,
                'Processing Time': processing_time
            })

            machine_available_time[best_machine] = start + processing_time
            job_completion_time[job_id] = start + processing_time
            job_current_operation[job_id] += 1

        available_operations = []
        for op in operations:
            if op['op_idx'] == job_current_operation[op['job_id']]:
                is_scheduled = False
                for job_schedule in schedule.values():
                    for scheduled_op in job_schedule:
                        if scheduled_op['Operation'] == op['op_idx'] and scheduled_op['Assigned Machine']:
                            is_scheduled = True
                            break
                    if is_scheduled:
                        break
                if not is_scheduled:
                    available_operations.append(op)

    return schedule
