
def heuristic(input_data):
    """Hybrid heuristic balancing makespan, job progress, and machine load."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {j: [] for j in range(1, n_jobs + 1)}
    machine_load = {m: 0 for m in range(n_machines)}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {job: 0 for job in range(1, n_jobs + 1)}
    eligible_ops = {job_id: 1 for job_id in range(1, n_jobs + 1)}

    operations = []
    for job_id, job_ops in jobs.items():
        for op_idx, (machines, times) in enumerate(job_ops):
            operations.append({
                'job': job_id,
                'operation': op_idx + 1,
                'machines': machines,
                'times': times
            })

    while operations:
        available_operations = [op for op in operations if op['operation'] == eligible_ops[op['job']]]

        if not available_operations:
            shortest_operation = min(operations, key=lambda op: min(op['times']))
            job_id = shortest_operation['job']
            op_num = shortest_operation['operation']
            machines = shortest_operation['machines']
            times = shortest_operation['times']
            best_machine, min_end_time, processing_time = None, float('inf'), 0

            for i, machine in enumerate(machines):
                start_time = max(machine_available_time[machine], job_completion_time[job_id])
                end_time = start_time + times[i] + 0.001 * machine_load[machine]
                if end_time < min_end_time:
                    min_end_time = end_time
                    best_machine = machine
                    processing_time = times[i]

            start_time = max(machine_available_time[best_machine], job_completion_time[job_id])
            end_time = start_time + processing_time
            schedule[job_id].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': processing_time
            })

            machine_available_time[best_machine] = end_time
            machine_load[best_machine] += processing_time
            job_completion_time[job_id] = end_time
            eligible_ops[job_id] += 1
            operations.remove(shortest_operation)
            continue

        best_operation, best_machine, earliest_finish, processing_time = None, None, float('inf'), 0

        for operation in available_operations:
            job_id = operation['job']
            op_num = operation['operation']
            machines = operation['machines']
            times = operation['times']
            for i, machine in enumerate(machines):
                start_time = max(machine_available_time[machine], job_completion_time[job_id])
                finish_time = start_time + times[i]
                weighted_finish = 0.7 * finish_time + 0.3 * machine_load[machine]

                if weighted_finish < earliest_finish:
                    earliest_finish = weighted_finish
                    best_operation = operation
                    best_machine = machine
                    processing_time = times[i]

        job_id = best_operation['job']
        op_num = best_operation['operation']

        start_time = max(machine_available_time[best_machine], job_completion_time[job_id])
        end_time = start_time + processing_time

        schedule[job_id].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

        machine_available_time[best_machine] = end_time
        machine_load[best_machine] += processing_time
        job_completion_time[job_id] = end_time
        eligible_ops[job_id] += 1
        operations.remove(best_operation)

    return schedule
