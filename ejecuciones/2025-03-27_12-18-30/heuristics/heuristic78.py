
def heuristic(input_data):
    """Balances earliest start and machine utilization."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}

    remaining_operations = {}
    for job in range(1, n_jobs + 1):
        remaining_operations[job] = [(i + 1, op) for i, op in enumerate(jobs[job])]

    while any(remaining_operations.values()):
        eligible_operations = []
        for job, ops in remaining_operations.items():
            if ops:
                eligible_operations.append((job, ops[0]))

        best_operation = None
        best_machine = None
        min_combined_score = float('inf')

        for job, (op_num, (machines, times)) in eligible_operations:
            for i, m in enumerate(machines):
                start_time = max(machine_time[m], job_completion_time[job])
                processing_time = times[i]
                # Combined score: weighted sum of start time and machine avail.
                combined_score = start_time + machine_time[m]
                if combined_score < min_combined_score:
                    min_combined_score = combined_score
                    best_operation = (job, (op_num, (machines, times)))
                    best_machine = m
                    best_processing_time = processing_time
                    best_start_time = start_time

        if best_operation is not None and best_machine is not None:
            job, (op_num, (machines, times)) = best_operation
            start = best_start_time
            end = start + best_processing_time
            m = best_machine

            if job not in schedule:
                schedule[job] = []
            schedule[job].append({'Operation': op_num, 'Assigned Machine': m, 'Start Time': start, 'End Time': end, 'Processing Time': best_processing_time})

            machine_time[m] = end
            job_completion_time[job] = end
            remaining_operations[job].pop(0)

    return schedule
