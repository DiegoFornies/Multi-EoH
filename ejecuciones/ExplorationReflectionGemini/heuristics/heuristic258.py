
def heuristic(input_data):
    """Dynamically prioritizes jobs based on remaining work and machine load."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}
    schedule = {j: [] for j in range(1, n_jobs + 1)}
    remaining_job_times = {}

    # Precompute total processing time for each job.
    for job_id in range(1, n_jobs + 1):
        total_time = sum(min(times) for machines, times in jobs[job_id])
        remaining_job_times[job_id] = total_time

    # Create a list of runnable operations.
    runnable_operations = []
    for job_id in range(1, n_jobs + 1):
        runnable_operations.append((job_id, 0)) # (job_id, operation_index)

    while runnable_operations:
        # Prioritize operations dynamically.
        best_operation = None
        best_priority = float('inf')

        for job_id, operation_index in runnable_operations:
            machines, times = jobs[job_id][operation_index]

            # Find the machine with the earliest available time.
            earliest_machine = None
            earliest_start_time = float('inf')
            processing_time = float('inf')

            for i, machine in enumerate(machines):
                start_time = max(machine_available_times[machine], job_completion_times[job_id])
                if start_time < earliest_start_time:
                    earliest_start_time = start_time
                    earliest_machine = machine
                    processing_time = times[i]

            # Dynamic priority: balance remaining job time and machine load.
            priority = (
                0.6 * (earliest_start_time + processing_time) +
                0.4 * machine_available_times[earliest_machine]
            )

            if priority < best_priority:
                best_priority = priority
                best_operation = (job_id, operation_index, earliest_machine, earliest_start_time, processing_time)

        # Schedule the best operation.
        job_id, operation_index, machine, start_time, processing_time = best_operation
        end_time = start_time + processing_time
        op_num = operation_index + 1

        schedule[job_id].append({
            'Operation': op_num,
            'Assigned Machine': machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

        # Update machine availability and job completion time.
        machine_available_times[machine] = end_time
        job_completion_times[job_id] = end_time
        remaining_job_times[job_id] -= processing_time

        # Remove the scheduled operation and add the next one (if any).
        runnable_operations.remove((job_id, operation_index))
        if operation_index + 1 < len(jobs[job_id]):
            runnable_operations.append((job_id, operation_index + 1))

    return schedule
