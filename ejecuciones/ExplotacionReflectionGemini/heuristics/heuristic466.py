
def heuristic(input_data):
    """Hybrid heuristic: SPT for makespan, then balance."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {job: [] for job in range(1, n_jobs + 1)}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_last_end_time = {j: 0 for j in range(1, n_jobs + 1)}
    machine_load = {m: 0 for m in range(n_machines)}

    remaining_operations = {j: len(jobs_data[j]) for j in range(1, n_jobs + 1)}
    scheduled_operations = set()

    operations = []
    for job_id in jobs_data:
        for op_idx, op_data in enumerate(jobs_data[job_id]):
            operations.append((job_id, op_idx, op_data))

    while any(remaining_operations[job] > 0 for job in range(1, n_jobs + 1)):
        eligible_operations = []
        for job_id, op_idx, op_data in operations:
            if job_id not in jobs_data:
                continue
            if remaining_operations[job_id] > 0 and (job_id, op_idx) not in scheduled_operations:
                is_next_operation = True
                if op_idx > 0:
                    if (job_id, op_idx - 1) not in scheduled_operations:
                        is_next_operation = False
                if is_next_operation:
                    eligible_operations.append((job_id, op_idx, op_data))

        if not eligible_operations:
            break

        best_operation = None
        min_makespan_priority = float('inf') #Modified to minimize makespan

        for job_id, op_idx, op_data in eligible_operations:
            machines, times = op_data

            best_machine = -1
            best_start_time = float('inf')
            best_time = float('inf')

            for i in range(len(machines)):
                machine = machines[i]
                time = times[i]
                start_time = max(machine_available_time[machine], job_last_end_time[job_id])
                end_time = start_time + time
                
                # Prioritize makespan.
                makespan_priority = end_time #Minimizing end time
                
                if makespan_priority < min_makespan_priority:
                    min_makespan_priority = makespan_priority
                    best_start_time = start_time
                    best_time = end_time
                    best_machine = machine

        job_id, op_idx, op_data, machine, start_time = best_operation = next((job_id, op_idx, op_data, m, max(machine_available_time[m], job_last_end_time[job_id])) for job_id, op_idx, op_data in eligible_operations for i, m in enumerate(op_data[0]) if max(machine_available_time[m], job_last_end_time[job_id]) + op_data[1][i] == min_makespan_priority)

        machines, times = op_data
        time = next(t for i, t in enumerate(times) if machines[i] == machine)
        end_time = start_time + time
        op_num = op_idx + 1

        schedule[job_id].append({
            'Operation': op_num,
            'Assigned Machine': machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': time
        })

        machine_available_time[machine] = end_time
        job_last_end_time[job_id] = end_time
        machine_load[machine] += time
        remaining_operations[job_id] -= 1
        scheduled_operations.add((job_id, op_idx))

    return schedule
