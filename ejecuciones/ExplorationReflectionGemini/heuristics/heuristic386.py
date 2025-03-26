
def heuristic(input_data):
    """Combines SPT and load balancing for FJSSP."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    machine_load = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in jobs}
    schedule = {j: [] for j in jobs}
    available_operations = []
    for job_id, operations in jobs.items():
        available_operations.append({'job': job_id, 'op_idx': 0})

    while available_operations:
        best_op = None
        best_weighted_time = float('inf')

        for op_data in available_operations:
            job_id = op_data['job']
            op_idx = op_data['op_idx']
            machines, times = jobs[job_id][op_idx]

            earliest_start_time = float('inf')
            selected_machine = None
            selected_time = None

            for machine_idx, (machine, time) in enumerate(zip(machines, times)):
                start_time = max(machine_available_times[machine], job_completion_times[job_id])
                end_time = start_time + time
                weighted_time = end_time + 0.05 * machine_load[machine]

                if weighted_time < earliest_start_time:
                    earliest_start_time = weighted_time
                    selected_machine = machine
                    selected_time = time
                    actual_start_time = start_time
                    actual_end_time = end_time

            if earliest_start_time < best_weighted_time:
                best_weighted_time = earliest_start_time
                best_op = op_data
                best_machine = selected_machine
                best_time = selected_time
                best_start_time = actual_start_time
                best_end_time = actual_end_time

        job_id = best_op['job']
        op_idx = best_op['op_idx']
        op_num = op_idx + 1

        schedule[job_id].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': best_start_time,
            'End Time': best_end_time,
            'Processing Time': best_time
        })

        machine_available_times[best_machine] = best_end_time
        machine_load[best_machine] += best_time
        job_completion_times[job_id] = best_end_time

        available_operations.remove(best_op)
        if op_idx + 1 < len(jobs[job_id]):
            available_operations.append({'job': job_id, 'op_idx': op_idx + 1})

    return schedule
