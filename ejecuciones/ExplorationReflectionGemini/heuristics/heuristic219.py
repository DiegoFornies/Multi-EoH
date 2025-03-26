
def heuristic(input_data):
    """Schedules jobs using dynamic SPT and load balancing."""

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in jobs}
    machine_load = {m: 0 for m in range(n_machines)} # Track machine load
    schedule = {j: [] for j in jobs}

    available_operations = []
    for job_id, operations in jobs.items():
        available_operations.append({'job': job_id, 'op_idx': 0})

    while available_operations:
        # Dynamically prioritize operations
        best_op = None
        best_score = float('inf')

        for op_data in available_operations:
            job_id = op_data['job']
            op_idx = op_data['op_idx']
            machines, times = jobs[job_id][op_idx]

            # Evaluate each possible machine assignment
            for machine_idx, (machine, time) in enumerate(zip(machines, times)):
                start_time = max(machine_available_times[machine], job_completion_times[job_id])
                processing_time = time
                
                # Calculate a score based on SPT and load balancing
                # Favor shorter processing times and less loaded machines
                # The weighting can be dynamically adjusted (this is a simplified example)
                load_factor = machine_load[machine] / (sum(machine_load.values()) + 1e-6) if sum(machine_load.values()) > 0 else 0
                score = processing_time + 10 * load_factor + start_time # Adjust 10 to influence load balancing importance

                if score < best_score:
                    best_score = score
                    best_op = op_data
                    best_machine = machine
                    best_time = time
                    best_start_time = start_time

        # Schedule the best operation
        job_id = best_op['job']
        op_idx = best_op['op_idx']
        op_num = op_idx + 1

        start_time = best_start_time
        end_time = start_time + best_time

        schedule[job_id].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_time
        })

        # Update machine availability, job completion time, and machine load
        machine_available_times[best_machine] = end_time
        job_completion_times[job_id] = end_time
        machine_load[best_machine] += best_time

        # Remove the scheduled operation and add the next operation (if any)
        available_operations.remove(best_op)
        if op_idx + 1 < len(jobs[job_id]):
            available_operations.append({'job': job_id, 'op_idx': op_idx + 1})

    return schedule
