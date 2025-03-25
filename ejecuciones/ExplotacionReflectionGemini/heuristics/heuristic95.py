
def heuristic(input_data):
    """Hybrid heuristic for FJSSP: balances machine load and job dependencies."""
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
        min_makespan = float('inf')
        # min_remaining = float('inf')

        for job_id, op_idx, op_data in eligible_operations:
            machines, times = op_data

            best_machine = -1
            best_start_time = float('inf')
            best_time = float('inf')
            proc_time = float('inf')

            for i in range(len(machines)):
                machine = machines[i]
                time = times[i]
                start_time = max(machine_available_time[machine], job_last_end_time[job_id])
                end_time = start_time + time

                if start_time < best_start_time: #earliest starting time for operation for balancing machine load
                    best_start_time = start_time
                    best_time = end_time
                    best_machine = machine
                    proc_time = time


            if best_time < min_makespan: #better makespan time
                min_makespan = best_time
                best_operation = (job_id, op_idx, op_data, best_machine, best_start_time, proc_time) # include the processing time

        # Schedule the best operation.

        if best_operation is not None:
            job_id, op_idx, op_data, machine, start_time, time = best_operation # unpacking here

            end_time = start_time + time # calculate end time based on scheduled info
            op_num = op_idx + 1

            schedule[job_id].append({'Operation': op_num, 'Assigned Machine': machine, 'Start Time': start_time, 'End Time': end_time, 'Processing Time': time})

            machine_available_time[machine] = end_time
            job_last_end_time[job_id] = end_time
            remaining_operations[job_id] -= 1
            scheduled_operations.add((job_id, op_idx)) #ensure not reschedule

    return schedule
