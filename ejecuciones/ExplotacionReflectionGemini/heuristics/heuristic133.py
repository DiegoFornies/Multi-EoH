
def heuristic(input_data):
    """Combines machine load and idle time to schedule jobs."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_available_times = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in range(1, n_jobs + 1)}
    solution = {}
    for job_id in jobs:
        solution[job_id] = []

    eligible_operations = []
    for job, operations in jobs.items():
        eligible_operations.append((job, 0))

    while eligible_operations:
        best_operation = None
        min_end_time = float('inf')

        for job, op_idx in eligible_operations:
            machines, times = jobs[job][op_idx]

            best_machine = None
            best_processing_time = None
            local_min_end = float('inf')

            for i in range(len(machines)):
                machine = machines[i]
                processing_time = times[i]

                start_time = max(machine_available_times[machine], job_completion_times[job])
                end_time = start_time + processing_time

                if end_time < local_min_end:
                    local_min_end = end_time
                    best_machine = machine
                    best_processing_time = processing_time

            if local_min_end < min_end_time:
                min_end_time = local_min_end
                best_operation = (job, op_idx, best_machine, best_processing_time)

        job, op_idx, assigned_machine, processing_time = best_operation
        start_time = max(machine_available_times[assigned_machine], job_completion_times[job])
        end_time = start_time + processing_time

        solution[job].append({
            'Operation': op_idx + 1,
            'Assigned Machine': assigned_machine,
            'Start Time': start_time,
            'End Time': end_time,
            'Processing Time': processing_time
        })

        machine_available_times[assigned_machine] = end_time
        job_completion_times[job] = end_time
        eligible_operations.remove((job, op_idx))

        if op_idx + 1 < len(jobs[job]):
            eligible_operations.append((job, op_idx + 1))

    return solution
