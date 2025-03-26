
def heuristic(input_data):
    """Combines earliest availability and SPT for FJSSP."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {job: 0 for job in range(1, n_jobs + 1)}
    job_remaining_time = {job: sum(min(t) for _, t in ops) for job, ops in jobs.items()}

    for job in range(1, n_jobs + 1):
        schedule[job] = []

    eligible_operations = []
    for job in range(1, n_jobs + 1):
        if jobs[job]:  # if job has operations
            eligible_operations.append((job, 0))  # (job, operation index)

    while eligible_operations:
        # Sort by SPT (remaining job time)
        eligible_operations.sort(key=lambda x: job_remaining_time[x[0]])

        job, op_idx = eligible_operations.pop(0)
        operation = jobs[job][op_idx]
        machines, times = operation
        op_num = op_idx + 1

        best_machine = None
        min_completion_time = float('inf')

        # Find machine minimizing completion time
        for i, machine in enumerate(machines):
            processing_time = times[i]
            start_time = max(machine_available_time[machine], job_completion_time[job])
            completion_time = start_time + processing_time

            if completion_time < min_completion_time:
                min_completion_time = completion_time
                best_machine = machine
                best_processing_time = processing_time
                best_start_time = start_time

        # Assign to best machine
        schedule[job].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': best_start_time,
            'End Time': best_start_time + best_processing_time,
            'Processing Time': best_processing_time
        })

        # Update machine availability and job completion time
        machine_available_time[best_machine] = best_start_time + best_processing_time
        job_completion_time[job] = best_start_time + best_processing_time
        job_remaining_time[job] -= best_processing_time

        # Add next operation to eligible operations
        if op_idx + 1 < len(jobs[job]):
            eligible_operations.append((job, op_idx + 1))

    return schedule
