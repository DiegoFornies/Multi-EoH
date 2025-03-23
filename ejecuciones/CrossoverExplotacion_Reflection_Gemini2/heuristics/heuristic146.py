
def heuristic(input_data):
    """Combines SPT, least loaded machine, dynamic delay, and remaining ops."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {j: [] for j in range(1, n_jobs + 1)}
    machine_load = {m: 0 for m in range(n_machines)}
    scheduled_operations = {j: 0 for j in range(1, n_jobs + 1)}

    operations = []
    for job_id, job_ops in jobs_data.items():
        for op_idx, (machines, times) in enumerate(job_ops):
            operations.append({
                'job': job_id,
                'operation': op_idx + 1,
                'machines': machines,
                'times': times
            })

    while True:
        eligible_operations = []
        for operation in operations:
            if operation['operation'] == scheduled_operations[operation['job']] + 1:
                eligible_operations.append(operation)

        if not eligible_operations:
            remaining_ops = [op for op in operations if op['operation'] > scheduled_operations[op['job']]]
            if not remaining_ops:
                break

            shortest_remaining_op = min(remaining_ops, key = lambda op: min(op['times']))

            job_id = shortest_remaining_op['job']
            op_num = shortest_remaining_op['operation']
            machines = shortest_remaining_op['machines']
            times = shortest_remaining_op['times']

            # Dynamic delay factor based on machine load variance
            load_values = list(machine_load.values())
            if load_values:
                load_variance = sum([(x - sum(load_values) / len(load_values)) ** 2 for x in load_values]) / len(load_values)
                delay_factor = 0.01 * load_variance
            else:
                delay_factor = 0.01
            
            best_machine = None
            min_completion_time = float('inf')
            processing_time = 0

            for i, machine in enumerate(machines):
                start_time = max(machine_available_times[machine], job_completion_times[job_id])
                completion_time = start_time + times[i] + machine_load[machine] * delay_factor
                
                if completion_time < min_completion_time:
                    min_completion_time = completion_time
                    best_machine = machine
                    processing_time = times[i]

            start_time = max(machine_available_times[best_machine], job_completion_times[job_id])
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

            machine_available_times[best_machine] = end_time
            job_completion_times[job_id] = end_time
            scheduled_operations[job_id] = op_num
            machine_load[best_machine] += processing_time
            operations.remove(shortest_remaining_op)
        else:
            best_operation = None
            best_machine = None
            min_completion_time = float('inf')
            processing_time = 0

            # Dynamic delay factor based on machine load variance
            load_values = list(machine_load.values())
            if load_values:
                load_variance = sum([(x - sum(load_values) / len(load_values)) ** 2 for x in load_values]) / len(load_values)
                delay_factor = 0.01 * load_variance
            else:
                delay_factor = 0.01

            for operation in eligible_operations:
                job_id = operation['job']
                op_num = operation['operation']
                machines = operation['machines']
                times = operation['times']

                for i, machine in enumerate(machines):
                    start_time = max(machine_available_times[machine], job_completion_times[job_id])
                    completion_time = start_time + times[i] + machine_load[machine] * delay_factor

                    if completion_time < min_completion_time:
                        min_completion_time = completion_time
                        best_machine = machine
                        best_operation = operation
                        processing_time = times[i]

            job_id = best_operation['job']
            op_num = best_operation['operation']

            start_time = max(machine_available_times[best_machine], job_completion_times[job_id])
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

            machine_available_times[best_machine] = end_time
            job_completion_times[job_id] = end_time
            scheduled_operations[job_id] = op_num
            machine_load[best_machine] += processing_time

            operations.remove(best_operation)

    return schedule
