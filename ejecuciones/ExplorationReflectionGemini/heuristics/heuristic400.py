
def heuristic(input_data):
    """Schedules jobs using a hybrid heuristic: SPT with load balancing."""

    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_load = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in jobs}
    schedule = {j: [] for j in jobs}

    available_operations = []
    for job_id, operations in jobs.items():
        available_operations.append({'job': job_id, 'op_idx': 0})

    while available_operations:
        # Find best op based on SPT and machine load.
        best_op = None
        best_score = float('inf')
        best_machine = None
        best_time = None

        for op_data in available_operations:
            job_id = op_data['job']
            op_idx = op_data['op_idx']
            machines, times = jobs[job_id][op_idx]

            for machine_idx, (machine, time) in enumerate(zip(machines, times)):
                start_time = max(machine_load[machine], job_completion_times[job_id])
                processing_time = time

                # Score is SPT + Load balancing, weights can be tuned.
                score = processing_time + 0.1 * machine_load[machine]  

                if score < best_score:
                    best_score = score
                    best_op = op_data
                    best_machine = machine
                    best_time = time

        # Schedule the best operation
        job_id = best_op['job']
        op_idx = best_op['op_idx']
        op_num = op_idx + 1

        start_time = max(machine_load[best_machine], job_completion_times[job_id])
        end_time = start_time + best_time

        schedule[job_id].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_time
        })

        # Update machine load and job completion time
        machine_load[best_machine] = end_time
        job_completion_times[job_id] = end_time

        # Remove scheduled operation & add the next
        available_operations.remove(best_op)
        if op_idx + 1 < len(jobs[job_id]):
            available_operations.append({'job': job_id, 'op_idx': op_idx + 1})

    return schedule
