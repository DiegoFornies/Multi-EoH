
def heuristic(input_data):
    """Combines min workload & earliest avail time, SPT, with dynamic delay."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_load = {m: 0 for m in range(n_machines)}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {job: 0 for job in range(1, n_jobs + 1)}

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
        # Prioritize operations that are next in their job sequence
        eligible_operations = []
        for operation in operations:
            job_id = operation['job']
            op_num = operation['operation']

            scheduled_count = 0
            if job_id in schedule:
                scheduled_count = len(schedule[job_id])
            
            if op_num == scheduled_count + 1:
                eligible_operations.append(operation)
        
        if not eligible_operations:
            # If no immediately feasible operations, choose the shortest remaining operation
            shortest_remaining_op = min(operations, key=lambda op: min(op['times']))
            job_id = shortest_remaining_op['job']
            op_num = shortest_remaining_op['operation']
            machines = shortest_remaining_op['machines']
            times = shortest_remaining_op['times']
        else:
            # Choose shortest processing time operation from eligible ones.
            shortest_remaining_op = min(eligible_operations, key=lambda op: min(op['times']))
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

        # Find the best machine
        best_machine = None
        min_combined_score = float('inf')

        for m_idx, machine in enumerate(machines):
            processing_time = times[m_idx]
            start_time = max(machine_available_time[machine], job_completion_time[job_id])
            end_time = start_time + processing_time
            load_penalty = machine_load[machine] * delay_factor  # Load aware penalty
            combined_score = machine_load[machine] + end_time + load_penalty

            if combined_score < min_combined_score:
                min_combined_score = combined_score
                best_machine = machine
                best_processing_time = processing_time
                best_start_time = start_time

        if job_id not in schedule:
            schedule[job_id] = []

        schedule[job_id].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': best_start_time,
            'End Time': best_start_time + best_processing_time,
            'Processing Time': best_processing_time
        })

        machine_load[best_machine] += best_processing_time
        machine_available_time[best_machine] = best_start_time + best_processing_time
        job_completion_time[job_id] = best_start_time + best_processing_time
        operations.remove(shortest_remaining_op)

    return schedule
