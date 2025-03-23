
def heuristic(input_data):
    """Combines EFT, SPT, and machine load balancing for FJSSP."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_load = {m: 0 for m in range(n_machines)}
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
            min_combined_score = float('inf')
            processing_time = 0
            
            load_values = list(machine_load.values())
            if load_values:
                load_variance = sum([(x - sum(load_values) / len(load_values)) ** 2 for x in load_values]) / (len(load_values) + 1e-6)
                delay_factor = 0.01 * load_variance
            else:
                delay_factor = 0.01

            for i, machine in enumerate(machines):
                start_time = max(machine_available_time[machine], job_last_end_time[job_id])
                finish_time = start_time + times[i]
                # Weighted finish time considering SPT and machine load
                weighted_finish = 0.7 * finish_time + 0.3 * machine_load[machine]
                # Add a load penalty to discourage overloading machines
                load_penalty = machine_load[machine] * delay_factor
                # Add small random noise to break ties
                combined_score = weighted_finish + load_penalty + machine * 0.0001

                if combined_score < min_combined_score:
                    min_combined_score = combined_score
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
            machine_load[best_machine] += processing_time
            job_last_end_time[job_id] = end_time
            scheduled_operations[job_id] = op_num
            operations.remove(shortest_operation)
            continue

        best_operation = None
        best_machine = None
        min_combined_score = float('inf')
        processing_time = 0

        load_values = list(machine_load.values())
        if load_values:
            load_variance = sum([(x - sum(load_values) / len(load_values)) ** 2 for x in load_values]) / (len(load_values) + 1e-6)
            delay_factor = 0.01 * load_variance
        else:
            delay_factor = 0.01

        for operation in eligible_operations:
            job_id = operation['job']
            op_num = operation['operation']
            machines = operation['machines']
            times = operation['times']

            for i, machine in enumerate(machines):
                start_time = max(machine_available_time[machine], job_last_end_time[job_id])
                finish_time = start_time + times[i]
                weighted_finish = 0.7 * finish_time + 0.3 * machine_load[machine]
                load_penalty = machine_load[machine] * delay_factor
                combined_score = weighted_finish + load_penalty + machine*0.0001

                if combined_score < min_combined_score:
                    min_combined_score = combined_score
                    best_operation = operation
                    best_machine = machine
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
        machine_load[best_machine] += processing_time
        job_last_end_time[job_id] = end_time
        scheduled_operations[job_id] = op_num

        operations.remove(best_operation)

    return schedule
