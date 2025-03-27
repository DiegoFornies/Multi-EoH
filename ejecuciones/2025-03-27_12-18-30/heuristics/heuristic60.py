
def heuristic(input_data):
    """
    Adaptive heuristic combining SPT, earliest machine, and remaining ops.
    """
    n_jobs = input_data['n_jobs']
    n_machines = input_data['n_machines']
    jobs = input_data['jobs']

    schedule = {}
    machine_time = {m: 0 for m in range(n_machines)}
    job_completion_time = {j: 0 for j in range(1, n_jobs + 1)}
    remaining_ops = {j: len(jobs[j]) for j in range(1, n_jobs + 1)}

    operation_queue = []
    for job, ops in jobs.items():
        operation_queue.append((job, 0))

    while operation_queue:
        best_job, best_op_idx = None, None
        min_weighted_makespan = float('inf')

        for job, op_idx in operation_queue:
            machines, times = jobs[job][op_idx]
            best_machine_local, best_start_time_local, best_processing_time_local = None, float('inf'), None

            for i, m in enumerate(machines):
                start_time = max(machine_time[m], job_completion_time[job])
                processing_time = times[i]

                if start_time < best_start_time_local:
                    best_start_time_local = start_time
                    best_machine_local = m
                    best_processing_time_local = processing_time

            makespan_impact = best_start_time_local + best_processing_time_local
            #Prioritize jobs with more remaining operations
            weight = remaining_ops[job] #Jobs with more remaining tasks have higher priority
            weighted_makespan = makespan_impact / weight

            if weighted_makespan < min_weighted_makespan:
                min_weighted_makespan = weighted_makespan
                best_job, best_op_idx = job, op_idx

        job = best_job
        op_idx = best_op_idx
        operation_queue.remove((job, op_idx))

        machines, times = jobs[job][op_idx]
        op_num = op_idx + 1

        best_machine, best_start_time, best_processing_time = None, float('inf'), None

        for i, m in enumerate(machines):
            start_time = max(machine_time[m], job_completion_time[job])
            processing_time = times[i]

            if start_time < best_start_time:
                best_start_time = start_time
                best_machine = m
                best_processing_time = processing_time

        start = best_start_time
        end = start + best_processing_time
        m = best_machine

        if job not in schedule:
            schedule[job] = []
        schedule[job].append({'Operation': op_num, 'Assigned Machine': m, 'Start Time': start, 'End Time': end, 'Processing Time': best_processing_time})

        machine_time[m] = end
        job_completion_time[job] = end
        remaining_ops[job] -= 1

        if op_idx + 1 < len(jobs[job]):
            operation_queue.append((job, op_idx + 1))

    return schedule
