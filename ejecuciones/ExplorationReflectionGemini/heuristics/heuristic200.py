
def heuristic(input_data):
    """Schedules jobs considering shortest processing time and machine load, dynamically adjusting priorities."""

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in jobs}
    machine_load = {m: 0 for m in range(n_machines)}  # Keep track of machine load
    schedule = {j: [] for j in jobs}

    available_operations = []
    for job_id, operations in jobs.items():
        available_operations.append({'job': job_id, 'op_idx': 0})

    while available_operations:
        # Prioritize operations based on a dynamic combination of SPT and machine load
        best_op = None
        best_score = float('inf')

        for op_data in available_operations:
            job_id = op_data['job']
            op_idx = op_data['op_idx']
            machines, times = jobs[job_id][op_idx]

            # Find the best machine for this operation, considering load
            best_machine = None
            best_time = None
            earliest_start_time = float('inf')

            for machine_idx, (machine, time) in enumerate(zip(machines, times)):
                start_time = max(machine_available_times[machine], job_completion_times[job_id])
                if start_time < earliest_start_time:
                    earliest_start_time = start_time
                    best_machine = machine
                    best_time = time

            # Calculate a score combining SPT and machine load (lower is better)
            processing_time = best_time
            load_factor = machine_load[best_machine] # Consider load
            score = processing_time + 0.1 * load_factor # Adjust the weight (0.1) as needed based on experiment

            if score < best_score:
                best_score = score
                best_op = op_data
                best_start_time = earliest_start_time
                best_processing_time = processing_time
                selected_machine = best_machine
                selected_time = best_time

        # Schedule the best operation
        job_id = best_op['job']
        op_idx = best_op['op_idx']
        op_num = op_idx + 1

        start_time = max(machine_available_times[selected_machine], job_completion_times[job_id])
        end_time = start_time + selected_time

        schedule[job_id].append({
            'Operation': op_num,
            'Assigned Machine': selected_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': selected_time
        })

        # Update machine availability, job completion time, and machine load
        machine_available_times[selected_machine] = end_time
        job_completion_times[job_id] = end_time
        machine_load[selected_machine] += selected_time

        # Remove the scheduled operation and add the next one
        available_operations.remove(best_op)
        if op_idx + 1 < len(jobs[job_id]):
            available_operations.append({'job': job_id, 'op_idx': op_idx + 1})

    return schedule
