
def heuristic(input_data):
    """Combines SPT and earliest machine availability for FJSSP."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs_data = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    job_remaining_times = {}
    job_ops = {j: 0 for j in range(1, n_jobs + 1)}

    # Calculate total processing time for each job.
    for job, operations in jobs_data.items():
        total_time = sum(min(times) for machines, times in operations)
        job_remaining_times[job] = total_time

    # Order jobs by remaining processing time (shortest first).
    job_order = sorted(job_remaining_times.keys(), key=job_remaining_times.get)

    scheduled_operations = 0
    total_operations = sum(len(job_data) for job_data in jobs_data.values())

    while scheduled_operations < total_operations:
        eligible_operations = []
        for job_id in job_order:
            op_idx = job_ops[job_id]
            if op_idx < len(jobs_data[job_id]):
                eligible_operations.append((job_id, op_idx))

        best_operation = None
        best_machine = None
        min_end_time = float('inf')

        for job_id, op_idx in eligible_operations:
            machines, times = jobs_data[job_id][op_idx]
            for m_idx, machine in enumerate(machines):
                processing_time = times[m_idx]
                start_time = max(machine_available_time[machine], job_completion_time[job_id])
                end_time = start_time + processing_time

                if end_time < min_end_time:
                    min_end_time = end_time
                    best_operation = (job_id, op_idx)
                    best_machine = machine
                    best_time = processing_time
                    best_start_time = start_time

        if best_operation is None:
            break

        job_id, op_idx = best_operation

        if job_id not in schedule:
            schedule[job_id] = []

        schedule[job_id].append({
            'Operation': op_idx + 1,
            'Assigned Machine': best_machine,
            'Start Time': best_start_time,
            'End Time': best_start_time + best_time,
            'Processing Time': best_time
        })

        machine_available_time[best_machine] = best_start_time + best_time
        job_completion_time[job_id] = best_start_time + best_time
        job_ops[job_id] += 1
        scheduled_operations += 1

    return schedule
