
def heuristic(input_data):
    """Prioritizes operations based on processing time and machine availability."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {j: [] for j in range(1, n_jobs + 1)}

    eligible_operations = []
    for job_id in range(1, n_jobs + 1):
        eligible_operations.append((job_id, 0))  # (job_id, op_idx)

    while eligible_operations:
        # Prioritize shortest processing time first
        eligible_operations.sort(key=lambda x: min(jobs_data[x[0]][x[1]][1]))

        job_id, op_idx = eligible_operations.pop(0)
        machines, processing_times = jobs_data[job_id][op_idx]
        op_num = op_idx + 1

        # Assign to machine that allows earliest completion
        best_machine = None
        min_end_time = float('inf')
        best_processing_time = None
        best_start_time = None

        for i, machine in enumerate(machines):
            processing_time = processing_times[i]
            start_time = max(machine_available_time[machine], job_completion_time[job_id])
            end_time = start_time + processing_time

            if end_time < min_end_time:
                min_end_time = end_time
                best_machine = machine
                best_processing_time = processing_time
                best_start_time = start_time

        schedule[job_id].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': best_start_time,
            'End Time': best_start_time + best_processing_time,
            'Processing Time': best_processing_time
        })

        machine_available_time[best_machine] = best_start_time + best_processing_time
        job_completion_time[job_id] = best_start_time + best_processing_time

        # Add next operation if it exists
        next_op_idx = op_idx + 1
        if next_op_idx < len(jobs_data[job_id]):
            eligible_operations.append((job_id, next_op_idx))

    return schedule
