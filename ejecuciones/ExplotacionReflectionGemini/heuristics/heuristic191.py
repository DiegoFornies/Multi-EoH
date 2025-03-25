
def heuristic(input_data):
    """Hybrid heuristic: SPT + machine load balancing + local search."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {job: [] for job in range(1, n_jobs + 1)}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_last_end_time = {j: 0 for j in range(1, n_jobs + 1)}

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
        min_makespan_increase = float('inf')

        for job_id, op_idx, op_data in eligible_operations:
            machines, times = op_data

            best_machine = -1
            min_operation_makespan = float('inf')
            operation_processing_time = float('inf')

            for i in range(len(machines)):
                machine = machines[i]
                time = times[i]
                start_time = max(machine_available_time[machine], job_last_end_time[job_id])
                end_time = start_time + time

                # Prioritize operations that minimize makespan increase.
                makespan_increase = max(0, end_time - max(machine_available_time.values(), default=0))

                if makespan_increase < min_makespan_increase:
                    min_makespan_increase = makespan_increase
                    min_operation_makespan = start_time
                    operation_processing_time = time
                    best_machine = machine
                    best_operation = (job_id, op_idx)

            if best_machine == -1:
                continue

        job_id, op_idx = best_operation

        machines, times = jobs_data[job_id][op_idx]

        machine = best_machine
        time = next(t for i, t in enumerate(times) if machines[i] == machine)

        start_time = max(machine_available_time[machine], job_last_end_time[job_id])
        end_time = start_time + time
        op_num = op_idx + 1

        schedule[job_id].append({'Operation': op_num, 'Assigned Machine': machine, 'Start Time': start_time, 'End Time': end_time, 'Processing Time': time})

        machine_available_time[machine] = end_time
        job_last_end_time[job_id] = end_time
        remaining_operations[job_id] -= 1
        scheduled_operations.add((job_id, op_idx))

    return schedule
