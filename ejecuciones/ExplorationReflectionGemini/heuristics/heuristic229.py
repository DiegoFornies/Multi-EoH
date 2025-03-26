
def heuristic(input_data):
    """Hybrid: SPT & Earliest Start, Machine load balancing."""
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
        min_weighted_time = float('inf')

        for op_data in available_operations:
            job_id = op_data['job']
            op_idx = op_data['op_idx']
            machines, times = jobs[job_id][op_idx]

            best_machine = None
            best_start_time = float('inf')
            best_processing_time = float('inf')

            for i in range(len(machines)):
                machine = machines[i]
                processing_time = times[i]
                start_time = max(machine_available_times[machine], job_completion_times[job_id])
                end_time = start_time + processing_time

                weighted_time = start_time + processing_time + 0.05 * machine_load[machine]

                if weighted_time < best_start_time + best_processing_time + 0.05 * machine_load[best_machine if best_machine else 0] if best_machine else weighted_time < float('inf'):
                    best_start_time = start_time
                    best_processing_time = processing_time
                    best_machine = machine

            weighted_time = best_start_time + best_processing_time + 0.05 * machine_load[best_machine]
            if weighted_time < min_weighted_time:
                min_weighted_time = weighted_time
                best_op = op_data
                selected_machine = best_machine
                selected_time = best_processing_time
                start_time = best_start_time


        job_id = best_op['job']
        op_idx = best_op['op_idx']
        op_num = op_idx + 1

        end_time = start_time + selected_time
        schedule[job_id].append({
            'Operation': op_num,
            'Assigned Machine': selected_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': selected_time
        })

        machine_available_times[selected_machine] = end_time
        machine_load[selected_machine] += selected_time
        job_completion_times[job_id] = end_time

        available_operations.remove(best_op)
        if op_idx + 1 < len(jobs[job_id]):
            available_operations.append({'job': job_id, 'op_idx': op_idx + 1})

    return schedule
