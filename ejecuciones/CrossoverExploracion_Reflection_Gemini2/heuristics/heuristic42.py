
def heuristic(input_data):
    """Combines machine load and shortest processing time for FJSSP."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_available_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    eligible_operations = []
    for job_id, operations in jobs.items():
        eligible_operations.append((job_id, 0))

    while eligible_operations:
        best_operation = None
        min_end_time = float('inf')

        for job_id, op_index in eligible_operations:
            machines, durations = jobs[job_id][op_index]

            for machine_id, duration in zip(machines, durations):
                start_time = max(machine_available_time[machine_id], job_completion_time[job_id])
                end_time = start_time + duration

                if end_time < min_end_time:
                    min_end_time = end_time
                    best_operation = (job_id, op_index, machine_id, duration, start_time)

        job_id, op_index, machine_id, duration, start_time = best_operation
        end_time = start_time + duration

        if job_id not in schedule:
            schedule[job_id] = []

        schedule[job_id].append({
            'Operation': op_index + 1,
            'Assigned Machine': machine_id,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': duration
        })

        machine_available_time[machine_id] = end_time
        job_completion_time[job_id] = end_time

        eligible_operations.remove((job_id, op_index))

        if op_index + 1 < len(jobs[job_id]):
            eligible_operations.append((job_id, op_index + 1))

    return schedule
