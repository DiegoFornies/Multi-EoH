
def heuristic(input_data):
    """Combines SPT and earliest machine availability for FJSSP."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_last_end_time = {j: 0 for j in range(1, n_jobs + 1)}
    scheduled_operations = {j: 0 for j in range(1, n_jobs + 1)}

    operations = []
    for job_id, job_ops in jobs.items():
        for op_idx, (machines, times) in enumerate(job_ops):
            operations.append({
                'job': job_id,
                'operation': op_idx + 1,
                'machines': machines,
                'times': times
            })

    operations.sort(key=lambda op: min(op['times']))

    while operations:
        eligible_operations = []
        for operation in operations:
            if operation['operation'] == scheduled_operations[operation['job']] + 1:
                eligible_operations.append(operation)

        if not eligible_operations:
            shortest_operation = min(operations, key=lambda op: min(op['times']))
            job_id = shortest_operation['job']
            op_num = shortest_operation['operation']
            machines = shortest_operation['machines']
            times = shortest_operation['times']

            best_machine = None
            min_end_time = float('inf')
            processing_time = 0

            for i, machine in enumerate(machines):
                start_time = max(machine_available_time[machine], job_last_end_time[job_id])
                end_time = start_time + times[i]

                if end_time < min_end_time:
                    min_end_time = end_time
                    best_machine = machine
                    processing_time = times[i]

            start_time = max(machine_available_time[best_machine], job_last_end_time[job_id])
            end_time = start_time + processing_time

            if job_id not in schedule:
                schedule[job_id] = []

            schedule[job_id].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': processing_time
            })

            machine_available_time[best_machine] = end_time
            job_last_end_time[job_id] = end_time
            scheduled_operations[job_id] = op_num

            operations.remove(shortest_operation)
            continue

        best_operation = None
        best_machine = None
        min_completion_time = float('inf')
        processing_time = 0

        for operation in eligible_operations:
            job_id = operation['job']
            op_num = operation['operation']
            machines = operation['machines']
            times = operation['times']

            for i, machine in enumerate(machines):
                start_time = max(machine_available_time[machine], job_last_end_time[job_id])
                completion_time = start_time + times[i]

                if completion_time < min_completion_time:
                    min_completion_time = completion_time
                    best_machine = machine
                    best_operation = operation
                    processing_time = times[i]

        if best_operation is None:
            break

        job_id = best_operation['job']
        op_num = best_operation['operation']

        start_time = max(machine_available_time[best_machine], job_last_end_time[job_id])
        end_time = start_time + processing_time

        if job_id not in schedule:
            schedule[job_id] = []

        schedule[job_id].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

        machine_available_time[best_machine] = end_time
        job_last_end_time[job_id] = end_time
        scheduled_operations[job_id] = op_num

        operations.remove(best_operation)

    return schedule
