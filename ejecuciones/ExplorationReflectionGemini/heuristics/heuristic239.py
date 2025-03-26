
def heuristic(input_data):
    """Schedules jobs adaptively, balancing makespan, load, and separation."""

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in jobs}
    schedule = {j: [] for j in jobs}

    available_operations = []
    for job_id, operations in jobs.items():
        available_operations.append({'job': job_id, 'op_idx': 0})

    while available_operations:
        # Adaptive priority: Consider makespan, machine load, and job separation.
        best_op = None
        best_score = float('inf')

        for op_data in available_operations:
            job_id = op_data['job']
            op_idx = op_data['op_idx']
            machines, times = jobs[job_id][op_idx]

            # Evaluate each machine option
            for machine_idx, (machine, time) in enumerate(zip(machines, times)):
                start_time = max(machine_available_times[machine], job_completion_times[job_id])
                end_time = start_time + time

                # Scoring function with dynamic weights (simplified)
                makespan_penalty = end_time # Minimize end time
                load_imbalance = machine_available_times[machine] # balance load
                separation_bonus = -start_time # keep close operations in one job

                # Adaptive weight (example): Adjust based on makespan progress
                makespan_weight = 0.5
                load_weight = 0.3
                separation_weight = 0.2

                score = makespan_weight * makespan_penalty + load_weight * load_imbalance + separation_weight * separation_bonus

                if score < best_score:
                    best_score = score
                    best_op = op_data
                    best_machine = machine
                    best_time = time
                    best_start_time = start_time
                    best_end_time = end_time
        
        # Schedule the best operation
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

        # Update machine availability and job completion time
        machine_available_times[best_machine] = best_end_time
        job_completion_times[job_id] = best_end_time

        # Remove the scheduled operation and add the next operation (if any)
        available_operations.remove(best_op)
        if op_idx + 1 < len(jobs[job_id]):
            available_operations.append({'job': job_id, 'op_idx': op_idx + 1})

    return schedule
