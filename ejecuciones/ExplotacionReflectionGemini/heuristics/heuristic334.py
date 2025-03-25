
def heuristic(input_data):
    """A hybrid heuristic combining SPT, machine load, and job dependencies."""
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
        min_combined_criteria = float('inf')

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
                combined_criteria = start_time + time * 0.5 + machine_load[machine] * 0.1 # Weighted criteria

                if combined_criteria < min_combined_criteria:
                    min_combined_criteria = combined_criteria
                    best_start_time = start_time
                    best_time = time
                    best_machine = machine
                    best_operation = (job_id, op_idx, op_data)

        if best_operation:
            job_id, op_idx, op_data = best_operation
            machines, times = op_data
            best_machine_index = machines.index(best_machine)
            time = times[best_machine_index]
            start_time = max(machine_available_time[best_machine], job_last_end_time[job_id])
            end_time = start_time + time
            op_num = op_idx + 1

            schedule[job_id].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': time
            })

            machine_available_time[best_machine] = end_time
            job_last_end_time[job_id] = end_time
            machine_load[best_machine] += time
            remaining_operations[job_id] -= 1
            scheduled_operations.add((job_id, op_idx))

    return schedule
