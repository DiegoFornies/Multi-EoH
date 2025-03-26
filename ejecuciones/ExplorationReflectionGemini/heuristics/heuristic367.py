
def heuristic(input_data):
    """Combines SPT and load balancing with lookahead."""
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    machine_load = {m: 0 for m in range(n_machines)}
    job_completion_times = {j: 0 for j in jobs}
    schedule = {j: [] for j in jobs}
    job_operations_scheduled = {job: 0 for job in jobs}

    while any(job_operations_scheduled[job] < len(jobs[job]) for job in jobs):
        eligible_operations = []
        for job in jobs:
            next_op_index = job_operations_scheduled[job]
            if next_op_index < len(jobs[job]):
                machines, times = jobs[job][next_op_index]
                eligible_operations.append((job, next_op_index, machines, times))

        if not eligible_operations:
            break

        best_op = None
        min_weighted_time = float('inf')

        for job, op_index, machines, times in eligible_operations:
            for i, m in enumerate(machines):
                start_time = max(job_completion_times[job], machine_load[m])
                weighted_time = start_time + times[i] + 0.05 * machine_load[m]
                if weighted_time < min_weighted_time:
                    min_weighted_time = weighted_time
                    best_op = (job, op_index, m, times[i])

        if best_op:
            job, op_index, best_machine, processing_time = best_op
            start_time = max(job_completion_times[job], machine_load[best_machine])
            end_time = start_time + processing_time
            op_num = op_index + 1

            schedule[job].append({
                'Operation': op_num,
                'Assigned Machine': best_machine,
                'Start Time': start_time,
                'End Time': end_time,
                'Processing Time': processing_time
            })

            machine_load[best_machine] = end_time
            job_completion_times[job] = end_time
            job_operations_scheduled[job] += 1

    return schedule
