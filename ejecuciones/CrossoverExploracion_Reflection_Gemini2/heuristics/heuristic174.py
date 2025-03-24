
def heuristic(input_data):
    """Schedules jobs using a modified Shortest Processing Time heuristic."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in jobs_data}
    schedule = {j: [] for j in jobs_data}
    next_operations = {}

    for job_id, job in jobs_data.items():
        next_operations[job_id] = 0  # Index of the next operation to schedule

    scheduled_count = 0
    total_operations = sum(len(job) for job in jobs_data.values())

    while scheduled_count < total_operations:
        eligible_operations = []
        for job_id in jobs_data:
            if next_operations[job_id] < len(jobs_data[job_id]):
                eligible_operations.append(job_id)

        if not eligible_operations:
            break

        # Find the operation with the shortest processing time amongst available operations
        best_job = None
        best_machine = None
        min_end_time = float('inf')
        processing_time = None

        for job_id in eligible_operations:
            op_idx = next_operations[job_id]
            machines, times = jobs_data[job_id][op_idx]

            for i in range(len(machines)):
                machine = machines[i]
                time = times[i]

                start_time = max(machine_available_time[machine], job_completion_time[job_id])
                end_time = start_time + time

                if end_time < min_end_time:
                    min_end_time = end_time
                    best_job = job_id
                    best_machine = machine
                    processing_time = time

        # Schedule the best operation
        if best_job is not None:
            job_id = best_job
            op_idx = next_operations[job_id]
            start_time = max(machine_available_time[best_machine], job_completion_time[job_id])
            end_time = start_time + processing_time

            schedule[job_id].append({
                'Operation': op_idx + 1,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': processing_time
            })

            machine_available_time[best_machine] = end_time
            job_completion_time[job_id] = end_time
            next_operations[job_id] += 1
            scheduled_count += 1

    return schedule
