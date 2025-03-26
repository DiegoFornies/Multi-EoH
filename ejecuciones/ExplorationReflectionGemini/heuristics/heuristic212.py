
def heuristic(input_data):
    """Combines SPT and load balancing dynamically."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_load = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in jobs}
    schedule = {j: [] for j in jobs}

    available_operations = []
    for job_id in jobs:
        available_operations.append((job_id, 0))  # (job_id, op_index)

    while available_operations:
        best_op = None
        best_score = float('inf')

        for job_id, op_idx in available_operations:
            machines, times = jobs[job_id][op_idx]
            op_num = op_idx + 1

            for i, m in enumerate(machines):
                start_time = max(job_completion_times[job_id], machine_load[m])
                processing_time = times[i]
                makespan_contribution = start_time + processing_time
                load_contribution = machine_load[m]
                
                # Dynamic weight based on machine load and operation duration.
                weight = 0.3 + 0.7 * (1 - (processing_time / (sum(min(t) for _, t in jobs[job_id]) + 1e-6)) if sum(min(t) for _, t in jobs[job_id])>0 else 0) # Favor shorter ops more when there is still more to process in current job
                score = weight * makespan_contribution + (1 - weight) * load_contribution # dynamically trade off between min makespan and balance

                if score < best_score:
                    best_score = score
                    best_op = (job_id, op_idx, m, start_time, processing_time)

        job_id, op_idx, best_machine, start_time, processing_time = best_op
        op_num = op_idx + 1
        end_time = start_time + processing_time

        schedule[job_id].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

        machine_load[best_machine] = end_time
        job_completion_times[job_id] = end_time

        available_operations.remove((job_id, op_idx))
        if op_idx + 1 < len(jobs[job_id]):
            available_operations.append((job_id, op_idx + 1))

    return schedule
