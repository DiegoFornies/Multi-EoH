
def heuristic(input_data):
    """Hybrid heuristic: Combines makespan and machine load balance."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {job: [] for job in range(1, n_jobs + 1)}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    operations = []
    for job_id in range(1, n_jobs + 1):
        for op_idx, op_data in enumerate(jobs[job_id]):
            operations.append((job_id, op_idx, op_data))

    while any(len(schedule[job_id]) < len(jobs[job_id]) for job_id in range(1, n_jobs + 1)):
        eligible_operations = []
        for job_id, op_idx, op_data in operations:
            if len(schedule[job_id]) == op_idx:
                eligible_operations.append((job_id, op_idx, op_data))

        if not eligible_operations:
            break

        best_operation = None
        min_score = float('inf')

        for job_id, op_idx, op_data in eligible_operations:
            machines, times = op_data
            for i, machine in enumerate(machines):
                processing_time = times[i]
                start_time = max(machine_available_time[machine], job_completion_time[job_id])
                end_time = start_time + processing_time
                # Primary objective: Minimize makespan
                # Secondary objective: Balance machine load (using a simple heuristic)
                machine_load_factor = machine_available_time[machine] / (sum(machine_available_time.values()) / n_machines + 1e-6) if sum(machine_available_time.values())>0 else 0
                score = end_time + 0.1 * machine_load_factor # Bias towards less loaded machines

                if score < min_score:
                    min_score = score
                    best_operation = (job_id, op_idx, machine, start_time, processing_time)

        if best_operation:
            job_id, op_idx, machine, start_time, processing_time = best_operation
            end_time = start_time + processing_time

            schedule[job_id].append({
                'Operation': op_idx + 1,
                'Assigned Machine': machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': processing_time
            })
            machine_available_time[machine] = end_time
            job_completion_time[job_id] = end_time

        else:
            break

    return schedule
