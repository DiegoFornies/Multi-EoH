
def heuristic(input_data):
    """Prioritizes operations with fewest machine choices."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {j: [] for j in range(1, n_jobs + 1)}

    eligible_operations = []
    for job_id in range(1, n_jobs + 1):
        eligible_operations.append((job_id, 0)) # (job_id, operation_index)

    while eligible_operations:
        # Prioritize ops with fewest machine choices
        eligible_operations.sort(key=lambda x: len(jobs[x[0]][x[1]][0]))
        job_id, operation_index = eligible_operations.pop(0)
        operation_data = jobs[job_id][operation_index]
        possible_machines = operation_data[0]
        possible_times = operation_data[1]

        # Choose machine with earliest available time
        best_machine = None
        min_start_time = float('inf')
        best_processing_time = None

        for i, machine in enumerate(possible_machines):
            processing_time = possible_times[i]
            start_time = max(machine_time[machine], job_completion_time[job_id])
            if start_time < min_start_time:
                min_start_time = start_time
                best_machine = machine
                best_processing_time = processing_time

        machine_time[best_machine] = min_start_time + best_processing_time
        job_completion_time[job_id] = min_start_time + best_processing_time

        schedule[job_id].append({
            'Operation': operation_index + 1,
            'Assigned Machine': best_machine,
            'Start Time': min_start_time,
            'End Time': min_start_time + best_processing_time,
            'Processing Time': best_processing_time
        })

        # Add next operation if available
        if operation_index + 1 < len(jobs[job_id]):
            eligible_operations.append((job_id, operation_index + 1))

    return schedule
