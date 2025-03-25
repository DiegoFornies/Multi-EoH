
def heuristic(input_data):
    """A heuristic for FJSSP combining SPT, machine load, and job order."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {job: [] for job in range(1, n_jobs + 1)}
    machine_available_time = {machine: 0 for machine in range(n_machines)}
    job_completion_time = {job: 0 for job in range(1, n_jobs + 1)}

    eligible_operations = []
    for job, operations in jobs.items():
        eligible_operations.append((job, 0))  # (job, operation_index)

    while eligible_operations:
        best_operation = None
        min_score = float('inf')

        for job, op_idx in eligible_operations:
            machines, times = jobs[job][op_idx]

            for i in range(len(machines)):
                machine = machines[i]
                time = times[i]
                start_time = max(machine_available_time[machine], job_completion_time[job])
                end_time = start_time + time
                score = end_time + machine_available_time[machine]/10  # SPT + machine load

                if score < min_score:
                    min_score = score
                    best_operation = (job, op_idx, machine, time)

        if best_operation:
            job, op_idx, assigned_machine, processing_time = best_operation
            start_time = max(machine_available_time[assigned_machine], job_completion_time[job])
            end_time = start_time + processing_time

            schedule[job].append({
                'Operation': op_idx + 1,
                'Assigned Machine': assigned_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': processing_time
            })

            machine_available_time[assigned_machine] = end_time
            job_completion_time[job] = end_time

            eligible_operations.remove((job, op_idx))

            if op_idx + 1 < len(jobs[job]):
                eligible_operations.append((job, op_idx + 1))

    return schedule
