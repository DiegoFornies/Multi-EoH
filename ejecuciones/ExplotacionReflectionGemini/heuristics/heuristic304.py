
def heuristic(input_data):
    """Schedules jobs by combining SPT and machine load balancing."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {job: [] for job in range(1, n_jobs + 1)}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_last_end_time = {j: 0 for j in range(1, n_jobs + 1)}
    machine_load = {m: 0 for m in range(n_machines)}

    remaining_operations = {j: len(jobs[j]) for j in range(1, n_jobs + 1)}
    scheduled_operations = set()

    operations = []
    for job_id in jobs:
        for op_idx in range(len(jobs[job_id])):
            operations.append((job_id, op_idx))

    while any(remaining_operations[job] > 0 for job in range(1, n_jobs + 1)):
        eligible_operations = []
        for job_id, op_idx in operations:
            if job_id not in jobs:
                continue
            if remaining_operations[job_id] > 0 and (job_id, op_idx) not in scheduled_operations:
                is_next_operation = True
                if op_idx > 0:
                    if (job_id, op_idx - 1) not in scheduled_operations:
                        is_next_operation = False
                if is_next_operation:
                    eligible_operations.append((job_id, op_idx))

        if not eligible_operations:
            break

        best_operation = None
        min_makespan_increase = float('inf')

        for job_id, op_idx in eligible_operations:
            machines, times = jobs[job_id][op_idx]

            best_machine = -1
            best_makespan_increase = float('inf')
            best_time = float('inf')

            for i, machine in enumerate(machines):
                time = times[i]
                start_time = max(machine_available_time[machine], job_last_end_time[job_id])
                end_time = start_time + time
                makespan_increase = end_time - machine_available_time[machine]

                if makespan_increase < best_makespan_increase:
                    best_makespan_increase = makespan_increase
                    best_time = time
                    best_machine = machine

            if best_makespan_increase < min_makespan_increase:
                min_makespan_increase = best_makespan_increase
                best_operation = (job_id, op_idx, best_machine, best_time)
            elif best_makespan_increase == min_makespan_increase:
                if machine_load[best_machine] < min(machine_load.values()):
                    min_makespan_increase = best_makespan_increase
                    best_operation = (job_id, op_idx, best_machine, best_time)

        job_id, op_idx, machine, time = best_operation
        start_time = max(machine_available_time[machine], job_last_end_time[job_id])
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
