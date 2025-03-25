
def heuristic(input_data):
    """FJSSP heuristic: Prioritizes machines and jobs based on time."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {job: [] for job in range(1, n_jobs + 1)}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    eligible_operations = []
    for job, operations in jobs.items():
        eligible_operations.append((job, 0))

    while eligible_operations:
        best_operation = None
        min_end_time = float('inf')

        for job, op_idx in eligible_operations:
            machines, times = jobs[job][op_idx]

            for i, machine in enumerate(machines):
                processing_time = times[i]
                start_time = max(machine_available_time[machine], job_completion_time[job])
                end_time = start_time + processing_time

                if end_time < min_end_time:
                    min_end_time = end_time
                    best_operation = (job, op_idx, job, machine, start_time, processing_time)

        job, op_idx, job_id, machine, start_time, processing_time = best_operation
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
        eligible_operations.remove((job, op_idx))

        if op_idx + 1 < len(jobs[job_id]):
            eligible_operations.append((job_id, op_idx + 1))

    return schedule
