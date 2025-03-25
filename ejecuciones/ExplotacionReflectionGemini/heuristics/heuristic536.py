
def heuristic(input_data):
    """Combines machine load balancing and earliest start time."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {job: [] for job in range(1, n_jobs + 1)}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    machine_load = {m: 0 for m in range(n_machines)}
    
    remaining_operations = {j: 1 for j in range(1, n_jobs + 1)}

    operations = []
    for job_id in jobs:
        for op_idx, op_data in enumerate(jobs[job_id]):
            operations.append((job_id, op_idx, op_data))

    scheduled_operations = set()

    while any(remaining_operations[job] > 0 for job in range(1, n_jobs + 1)):
        eligible_operations = []
        for job_id, op_idx, op_data in operations:
            if job_id not in jobs:
                continue
            if remaining_operations[job_id] > 0 and (job_id, op_idx) not in scheduled_operations:
                is_next_operation = True
                if op_idx > 0:
                    already_done = False
                    for d in schedule[job_id]:
                        if d['Operation']== op_idx :
                            already_done = True
                    if not already_done:
                        is_next_operation = False
                if is_next_operation:
                    eligible_operations.append((job_id, op_idx, op_data))

        if not eligible_operations:
            break

        best_operation = None
        min_start_time = float('inf')

        for job_id, op_idx, op_data in eligible_operations:
            machines, times = op_data

            best_machine = -1
            best_start_time = float('inf')

            for i in range(len(machines)):
                machine = machines[i]
                time = times[i]
                start_time = max(machine_available_time[machine], job_completion_time[job_id])
                end_time = start_time + time
                if start_time < best_start_time:
                    best_start_time = start_time
                    best_machine = machine
                    best_time = end_time
                elif start_time == best_start_time:
                    if machine_load[machine] < machine_load[best_machine]:
                        best_machine = machine
                        best_time = end_time

            if best_start_time < min_start_time:
                min_start_time = best_start_time
                best_operation = (job_id, op_idx, op_data, best_machine, best_start_time)

        job_id, op_idx, op_data, machine, start_time = best_operation
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
        job_completion_time[job_id] = end_time
        machine_load[machine] += time
        scheduled_operations.add((job_id, op_idx))
        if op_idx + 1 >= len(jobs[job_id]):
            remaining_operations[job_id]=0
        else:
            remaining_operations[job_id]=1

    return schedule
