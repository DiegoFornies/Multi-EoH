
def heuristic(input_data):
    """Schedules jobs by iteratively assigning operations to machines minimizing idle time."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in jobs}
    schedule = {j: [] for j in jobs}

    remaining_operations = {job_id: list(range(len(operations))) for job_id, operations in jobs.items()}

    while any(remaining_operations.values()):
        # Find the next operation to schedule
        best_job = None
        best_op_idx = None
        best_machine = None
        min_idle_time = float('inf')
        best_processing_time = None

        for job_id, ops in remaining_operations.items():
            if not ops:
                continue

            op_idx = ops[0]
            machines, times = jobs[job_id][op_idx]

            for machine_idx, (machine, time) in enumerate(zip(machines, times)):
                start_time = max(machine_available_times[machine], job_completion_times[job_id])
                idle_time = start_time - machine_available_times[machine]

                if idle_time < min_idle_time:
                    min_idle_time = idle_time
                    best_job = job_id
                    best_op_idx = op_idx
                    best_machine = machine
                    best_processing_time = time

        # Schedule the operation
        start_time = max(machine_available_times[best_machine], job_completion_times[best_job])
        end_time = start_time + best_processing_time
        op_num = best_op_idx + 1

        schedule[best_job].append({
            'Operation': op_num,
            'Assigned Machine': best_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': best_processing_time
        })

        # Update machine and job times
        machine_available_times[best_machine] = end_time
        job_completion_times[best_job] = end_time

        # Remove the scheduled operation
        remaining_operations[best_job].pop(0)
        if not remaining_operations[best_job]:
            del remaining_operations[best_job]

    return schedule
